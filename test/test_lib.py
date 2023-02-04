from markdown_sitegen.lib import get_root_path


def test_get_root_path():
    assert get_root_path('/') == ''
    assert get_root_path('/blog') == '../'
    assert get_root_path('/blog.html') == '../'
    assert get_root_path('/blog/') == '../'
    assert get_root_path('/blog/hello/world') == '../../../'
    assert get_root_path('/blog/hello/world.html') == '../../../'
    assert get_root_path('/blog/hello/world/') == '../../../'
