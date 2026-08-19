from contextlib import ExitStack

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph

from app.agents.graph.nodes import SupportGraphNodes
from app.agents.graph.routing import route_decision
from app.agents.graph.state import SupportState
from app.core.config import settings


class SupportWorkflow:

    def __init__(
        self,
        nodes: SupportGraphNodes | None = None,
    ) -> None:

        self.nodes = nodes or SupportGraphNodes()

        # Keep the PostgreSQL checkpointer context alive
        self._stack = ExitStack()

        self.checkpointer = self._stack.enter_context(
            PostgresSaver.from_conn_string(
                settings.checkpoint_database_url
            )
        )

        # Create required checkpoint tables
        self.checkpointer.setup()

        self.graph = self._build_graph()

    def _build_graph(self):

        builder = StateGraph(SupportState)

        builder.add_node(
            "classify",
            self.nodes.classify,
        )

        builder.add_node(
            "retrieve",
            self.nodes.retrieve,
        )

        builder.add_node(
            "investigate",
            self.nodes.investigate,
        )

        builder.add_node(
            "decide",
            self.nodes.decide,
        )

        builder.add_node(
            "respond",
            self.nodes.respond,
        )

        builder.add_node(
            "escalate",
            self.nodes.escalate,
        )

        builder.add_edge(
            START,
            "classify",
        )

        builder.add_edge(
            "classify",
            "retrieve",
        )

        builder.add_edge(
            "retrieve",
            "investigate",
        )

        builder.add_edge(
            "investigate",
            "decide",
        )

        builder.add_conditional_edges(
            "decide",
            route_decision,
            {
                "resolve": "respond",
                "escalate": "escalate",
            },
        )

        builder.add_edge(
            "respond",
            END,
        )

        builder.add_edge(
            "escalate",
            END,
        )

        return builder

    def compile(self):

        return self.graph.compile(
            checkpointer=self.checkpointer
        )

    def close(self) -> None:

        self._stack.close()