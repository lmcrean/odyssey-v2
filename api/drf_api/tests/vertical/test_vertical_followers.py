"""
Vertical Authentication Testing Suite

This module implements a vertical testing approach for posts,
progressing from simple unit tests to complex integration and endpoint tests.
Tests are ordered to run from basic functionality to complete user journeys.

The Vertical Authentication confirms that the following:
1. A user can follow another user
2. A user can unfollow another user
3. A user cannot follow themselves
4. A user can view their list of followers
5. A user can view their list of following
6. A user can view another user's followers
7. A user can view another user's following
8. Following counts are updated correctly
9. Follower counts are updated correctly
10. Following/unfollowing triggers appropriate notifications
11. Following relationships persist after user logout/login
12. Following status is correctly reflected in user profiles
"""