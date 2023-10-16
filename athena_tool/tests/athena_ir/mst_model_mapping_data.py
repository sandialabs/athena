import pyaml
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class Dataflow:
    Flow: list[str]


@dataclass
class InputLayer:
    Layer: str = "Conv2d-1"
    Type: str = "CONV"
    Stride: dict[str:int] = field(default_factory={"X": 2, "Y": 2})
    Dimensions: dict[str:int] = field(
        default_factory={"K": 32, "C": 3, "R": 3, "S": 3, "Y": 224, "X": 224}
    )


class MaestroLayer:
    def generate_layer_str(self):
        dim_str = "Dimensions {{ K: {:.0f}, C: {:.0f}, Y: {:.0f}, X: {:.0f}, R: {:.0f}, S: {:.0f} }}"


tx = """Dimensions { K: 32, C: 3, R: 3, S: 3, Y: 224, X: 224 }
Dataflow {
    TemporalMap (1,1) K;
TemporalMap (1,1) C;
TemporalMap (Sz(R),1) Y;
SpatialMap (Sz(S),1) X;
TemporalMap (Sz(R),Sz(R)) R;
TemporalMap (Sz(S),Sz(S)) S;
}"""
