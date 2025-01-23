"""
Vertical Likes Testing Suite

This module implements a vertical testing approach for likes,
progressing from simple unit tests to complex integration and endpoint tests.
Tests are ordered to run from basic functionality to complete user journeys.

The Vertical Likes Testing confirms that the following:
1. A user can like a post
2. A user can unlike a post
3. A user cannot like their own post
4. A user can view all likes on a post
5. A user can view all posts they have liked
6. Like counts are updated correctly on posts
7. Post authors receive notifications for new likes
8. Likes persist after user logout/login
9. Likes are properly deleted when parent post is deleted
10. A user cannot like the same post multiple times
11. Like status is correctly reflected in post details
12. Like timestamps are recorded correctly
13. Likes can be filtered by user
14. Likes can be filtered by post
15. Like counts are displayed correctly in user profiles
16. Like activity appears in user activity feed
""" 