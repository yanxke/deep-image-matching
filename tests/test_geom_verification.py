import numpy as np
import pytest

from deep_image_matching import GeometricVerification
from deep_image_matching.utils.geometric_verification import geometric_verification


@pytest.fixture
def tie_points():
    # Create two numpy array with shape (100, 2)
    rng = np.random.default_rng(12345)
    kpts0 = rng.random((100, 2))
    kpts1 = rng.random((100, 2))

    return kpts0, kpts1


def test_valid_inputs(tie_points):
    kpts0, kpts1 = tie_points
    method = GeometricVerification.PYDEGENSAC
    result = geometric_verification(
        kpts0=kpts0,
        kpts1=kpts1,
        method=method,
    )
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], np.ndarray)
    assert isinstance(result[1], np.ndarray)


def test_valid_method_name(tie_points):
    kpts0, kpts1 = tie_points
    method = "pydegensac"
    result = geometric_verification(
        kpts0=kpts0,
        kpts1=kpts1,
        method=method,
    )
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], np.ndarray)
    assert isinstance(result[1], np.ndarray)


def test_invalid_method_name(tie_points):
    kpts0, kpts1 = tie_points
    method = "invalid_method"
    with pytest.raises(ValueError):
        geometric_verification(kpts0=kpts0, kpts1=kpts1, method=method)


def test_essential_matrix_when_intrinsics_available():
    rng = np.random.default_rng(42)
    kpts0 = rng.uniform(0, 1000, size=(120, 2)).astype(np.float64)
    # small perturbation to keep correspondences plausible for robust estimation
    kpts1 = kpts0 + rng.normal(0, 0.8, size=(120, 2))
    K = np.array([[900.0, 0.0, 500.0], [0.0, 900.0, 500.0], [0.0, 0.0, 1.0]])

    model, inliers = geometric_verification(
        kpts0=kpts0,
        kpts1=kpts1,
        K0=K,
        K1=K,
        method=GeometricVerification.RANSAC,
    )

    assert isinstance(model, np.ndarray)
    assert isinstance(inliers, np.ndarray)
    assert model.shape[1] == 3
    assert len(inliers) == len(kpts0)


if __name__ == "__main__":
    pytest.main([__file__])
