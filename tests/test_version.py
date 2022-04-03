from collections_extended._version import __version__


def test_version_sem_ver():
	assert isinstance(__version__, str)
	parts = __version__.split(".")
	assert len(parts) == 3
