from blog.utils import rounded_timesince


def test_timesince_rounded(new_post):
    """
    Test rounded timesince func.
    """
    assert rounded_timesince(new_post.created_at) == '0 minutes'
