"""
Vertical Posts Testing Suite

This module implements a vertical testing approach for posts,
progressing from simple unit tests to complex integration and endpoint tests.
Tests are ordered to run from basic functionality to complete user journeys.

The Vertical Posts Testing confirms that the following:
1. A user can create a new post
2. A user can edit their own post
3. A user can delete their own post
4. A user cannot edit/delete other users' posts
5. A user can view all posts in the feed
6. A user can view a single post's details
7. A user can filter posts by following users
8. Posts display correct creation and update timestamps
9. Posts can contain text content
10. Posts can contain image content
11. Posts show correct author information
12. Posts maintain proper ordering in feeds
13. Posts persist after user logout/login
14. Post creation triggers appropriate notifications
15. Posts can be reported for inappropriate content
16. Posts respect character limits and content restrictions
"""