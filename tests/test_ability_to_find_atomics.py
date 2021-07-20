def test_art_user_paths(art_fixture_with_relative_path):
    assert '/Users/josh.rickard' in art_fixture_with_relative_path.atomics_path
