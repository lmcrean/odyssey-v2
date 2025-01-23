"""
Vertical Comments Testing Suite

This module implements a vertical testing approach for comments,
progressing from simple unit tests to complex integration and endpoint tests.
Tests are ordered to run from basic functionality to complete user journeys.

The Vertical Comments Testing confirms that the following:
1. A user can create a comment on a post
2. A user can edit their own comment
3. A user can delete their own comment
4. A user cannot edit/delete other users' comments
5. A user can view all comments on a post
6. Comments display correct creation and update timestamps
7. Comments show correct author information
8. Comments can be nested (replies to comments)
9. Comment authors receive notifications when someone replies
10. Post authors receive notifications for new comments
11. Comments persist after user logout/login
12. Comments can be reported for inappropriate content
13. Comments respect character limits
14. Comments maintain proper chronological ordering
15. Comments can be filtered by post
16. Comment counts are updated correctly on posts
17. Comments can contain text formatting
18. Comments are properly deleted when parent post is deleted
""" 