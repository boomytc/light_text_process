import pynini
from fun_text_processing.inverse_text_normalization.zh.utils import get_abs_path
from fun_text_processing.inverse_text_normalization.zh.graph_utils import (
    DAMO_SIGMA,
    GraphFst,
    convert_space,
    delete_extra_space,
    delete_space,
    get_singulars,
)
from pynini.lib import pynutil


class MeasureFst(GraphFst):
    """
    Finite state transducer for classifying measure
        e.g. minus twelve kilograms -> measure { negative: "true" cardinal { integer: "12" } units: "kg" }

    Args:
        cardinal: CardinalFst
        decimal: DecimalFst
    """

    def __init__(self, cardinal: GraphFst, decimal: GraphFst):
        super().__init__(name="measure", kind="classify")

        cardinal_graph = cardinal.graph_no_exception

        graph_unit_en = pynini.string_file(get_abs_path("data/measurements_en.tsv"))
        graph_unit_zh = pynini.string_file(get_abs_path("data/measurements_zh.tsv"))
        graph_sign = pynini.string_file(get_abs_path("data/numbers/sign.tsv"))

        graph_units = graph_unit_en | (
            (pynini.accep("亿") | pynini.accep("兆") | pynini.accep("万")).ques + graph_unit_zh
        )

        optional_graph_negative = pynini.closure(
            pynutil.insert("negative: ")
            + (pynini.cross("负", '"true"') | pynini.cross("负的", '"true"'))
            + delete_space,
            0,
            1,
        )

        unit_all = pynutil.insert('units: "') + graph_units + pynutil.insert('"')
        percent_unit = pynutil.insert('units: "%"')

        subgraph_decimal = (
            pynutil.insert("decimal { ")
            + optional_graph_negative
            + decimal.final_graph_wo_negative
            + pynutil.insert(" }")
            + pynutil.insert(" ")
            + unit_all
        )
        subgraph_cardinal = (
            pynutil.insert("cardinal { ")
            + optional_graph_negative
            + pynutil.insert('integer: "')
            + cardinal_graph
            + pynutil.insert('"')
            + pynutil.insert(" }")
            + pynutil.insert(" ")
            + unit_all
        )
        percent_prefix = pynutil.delete("百分") + pynutil.delete("之").ques
        percent_decimal = (
            pynutil.insert("decimal { ")
            + percent_prefix
            + decimal.final_graph_wo_negative
            + pynutil.insert(" }")
            + pynutil.insert(" ")
            + percent_unit
        )
        percent_cardinal = (
            pynutil.insert("cardinal { ")
            + pynutil.insert('integer: "')
            + percent_prefix
            + (cardinal_graph | pynini.cross("百", "100"))
            + pynutil.insert('"')
            + pynutil.insert(" }")
            + pynutil.insert(" ")
            + percent_unit
        )

        final_graph = subgraph_decimal | subgraph_cardinal | percent_decimal | percent_cardinal
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
