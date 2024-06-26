# Copyright 2024 Vlad Krupinskii <mrvladus@yandex.ru>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

from gi.repository import Adw  # type:ignore

from __main__ import APP_ID, PROFILE

if TYPE_CHECKING:
    from errands.application import ErrandsApplication
    from errands.lib.notifications import ErrandsNotificationsDaemon
    from errands.widgets.shared.datetime_window import DateTimeWindow
    from errands.widgets.shared.notes_window import NotesWindow
    from errands.widgets.sidebar import Sidebar
    from errands.widgets.tags.tags import Tags
    from errands.widgets.tags.tags_sidebar_row import TagsSidebarRow
    from errands.widgets.task import Task
    from errands.widgets.task_list.task_list import TaskList
    from errands.widgets.today.today import Today
    from errands.widgets.today.today_sidebar_row import TodaySidebarRow
    from errands.widgets.today.today_task import TodayTask
    from errands.widgets.trash.trash import Trash
    from errands.widgets.trash.trash_sidebar_row import TrashSidebarRow
    from errands.widgets.window import Window


class State:
    """Application's state class for accessing core widgets globally
    and some utils for quick access to deeper nested widgets"""

    # Constants
    PROFILE: str = PROFILE
    APP_ID: str = APP_ID

    # Notifications
    notifications_daemon: ErrandsNotificationsDaemon | None = None

    # Application
    application: ErrandsApplication | None = None

    # Main window
    main_window: Window | None = None
    split_view: Adw.NavigationSplitView | None = None

    # View Stack
    view_stack: Adw.ViewStack | None = None
    today_page: Today | None = None
    tags_page: Tags | None = None
    trash_page: Trash | None = None

    # Sidebar
    sidebar: Sidebar | None = None
    today_sidebar_row: TodaySidebarRow | None = None
    tags_sidebar_row: TagsSidebarRow | None = None
    trash_sidebar_row: TrashSidebarRow | None = None

    # Notes window
    notes_window: NotesWindow | None = None

    # Date and time window
    datetime_window: DateTimeWindow | None = None

    @classmethod
    def get_task_list(cls, uid: str) -> TaskList:
        return [lst for lst in cls.get_task_lists() if lst.list_uid == uid][0]

    @classmethod
    def get_task_lists(cls) -> list[TaskList]:
        """All Task Lists"""

        return cls.sidebar.task_lists

    @classmethod
    def get_tasks(cls) -> list[Task]:
        """All Tasks in all Task Lists"""

        all_tasks: list[Task] = []
        for list in cls.get_task_lists():
            all_tasks.extend(list.all_tasks)

        return all_tasks

    @classmethod
    def get_task(cls, list_uid: str, uid: str) -> Task:
        for list in cls.get_task_lists():
            if list.list_uid == list_uid:
                for task in list.all_tasks:
                    if task.uid == uid:
                        return task

    @classmethod
    def get_today_task(cls, list_uid: str, uid: str) -> TodayTask | None:
        for task in cls.today_page.tasks:
            if task.list_uid == list_uid and task.uid == uid:
                return task
        return None
