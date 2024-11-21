import threading
import time
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

class TaskLocker:
    def __init__(self, default_delay_seconds=None):
        self.default_delay_seconds = default_delay_seconds

    def lock_task(self, task_name, callback, delay_seconds=None, data=False):
        is_task_locked = cache.get(task_name)
        # print(f'lock ---> {task_name} = {is_task_locked}')
        
        if not is_task_locked:
            try:
                cache.set(task_name, True)
                result = callback()
                return result
            finally:
                delay_seconds = delay_seconds if delay_seconds is not None else self.default_delay_seconds
                if delay_seconds is not None:
                    threading.Thread(target=self._delay_and_delete_cache, args=(task_name, delay_seconds)).start()
                else:
                    cache.delete(task_name)
        elif data:
            result = callback()
            # print('Retornou dados com locked')
            return Response({'detail': 'locked', 'data': result.data}, status=status.HTTP_200_OK)
        else:
            # print('Retornou locked sem dados')
            return Response({'detail': 'locked'}, status=status.HTTP_200_OK)

    def _delay_and_delete_cache(self, task_name, delay_seconds):
        try:
            time.sleep(delay_seconds)
        finally:
            cache.delete(task_name)
            # print(f'unlock ---> {task_name}')
