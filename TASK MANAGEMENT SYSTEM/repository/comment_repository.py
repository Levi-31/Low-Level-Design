



from typing import Dict, List

from domain.comment import Comment


class CommentRepository:
    def __init__(self):
        self._comments: Dict[int, Comment] = {}
        self._next_id = 1

    def save(self, comment: Comment) -> Comment:
        if comment.id == 0:
            new_comment = Comment(self._next_id, comment.task_id, comment.user_id, comment.content)
            self._next_id += 1
            self._comments[new_comment.id] = new_comment
            return new_comment
            
        self._comments[comment.id] = comment
        return comment

    def find_by_task_id(self, task_id: int) -> List[Comment]:
        return [c for c in self._comments.values() if c.task_id == task_id]
