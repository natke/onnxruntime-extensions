import onnx
from onnx import onnx_pb as onnx_proto
from .._ocos import default_opset_domain, get_library_path  # noqa


class SingleOpTorch:
    @classmethod
    def get_next_id(cls):
        if not hasattr(cls, '_id_counter'):
            cls._id_counter = 0
        cls._id_counter += 1
        return cls._id_counter


    @classmethod
    def build_singleop_graph(cls, op_type, *args, **kwargs):
        inputs = [onnx.helper.make_tensor_value_info('input_text', onnx_proto.TensorProto.STRING, [None, None])]
        outputs = [onnx.helper.make_tensor_value_info("input_ids", onnx.TensorProto.INT64, [None, None])]
        cuop = onnx.helper.make_node(op_type,
                                     [i_.name for i_ in inputs],
                                     [o_.name for o_ in outputs],
                                     "{}_{}".format(op_type, cls.get_next_id()),
                                     domain=default_opset_domain())
        graph = onnx.helper.make_graph([cuop],
                                       "og_{}_{}".format(op_type, cls.get_next_id()),
                                       inputs,
                                       outputs)
        return graph
