"""
Vertical Messages Testing Suite

This module implements a vertical testing approach for direct messages,
progressing from simple unit tests to complex integration and endpoint tests.
Tests are ordered to run from basic functionality to complete user journeys.

The Vertical Messages Testing confirms that the following:
1. A user can send a direct message to another user
2. A user can receive messages from other users
3. A user can view their message inbox
4. A user can view their sent messages
5. A user can delete messages they've sent
6. Messages show correct sender and recipient information
7. Messages display correct timestamps
8. Users receive notifications for new messages
9. Messages persist after user logout/login
10. Messages can contain text content
11. Messages respect character limits
12. Users can block messages from specific users
13. Messages maintain proper chronological ordering
14. Users can view message read status
15. Users can mark messages as read/unread
16. Messages are properly threaded by conversation
17. Users can search through their message history
18. Messages support basic text formatting
19. Users can report inappropriate messages
20. Message counts are updated correctly in user profiles
""" 