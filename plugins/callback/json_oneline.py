# (c) 2016, Matt Martz <matt@sivel.net>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = '''
    callback: json_oneline
    short_description: Ansible screen output as single-line JSON
    version_added: "2.2"
    description:
        - This callback converts all events into JSON output to stdout, in a single line
    type: stdout
    requirements:
      - Set as stdout in config
    options:
      show_custom_stats:
        version_added: "2.6"
        name: Show custom stats
        description: 'This adds the custom stats set via the set_stats plugin to the play recap'
        default: False
        env:
          - name: ANSIBLE_SHOW_CUSTOM_STATS
        ini:
          - key: show_custom_stats
            section: defaults
        type: bool
'''

import datetime
from json import dumps

from ansible.parsing.ajson import AnsibleJSONEncoder

try:
    # JSON callback moved to ansible.posix collection for ansible >= 2.10
    from ansible_collections.ansible.posix.plugins.callback.json import CallbackModule as JSONCallbackModule
except ImportError as error:
    # JSON callback is bundled with ansible < 2.10
    from ansible.plugins.callback.json import CallbackModule as JSONCallbackModule

def current_time():
    return '%sZ' % datetime.datetime.utcnow().isoformat()

class CallbackModule(JSONCallbackModule):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'json_oneline'


    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics"""

        hosts = sorted(stats.processed.keys())

        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        custom_stats = {}
        global_custom_stats = {}

        if self.get_option('show_custom_stats') and stats.custom:
            custom_stats.update(dict((self._convert_host_to_name(k), v) for k, v in stats.custom.items()))
            global_custom_stats.update(custom_stats.pop('_run', {}))

        output = {
            'plays': [play['meta'] for play in self.results],
            'stats': summary,
            'custom_stats': custom_stats,
            'global_custom_stats': global_custom_stats,
        }
        self._display.display(dumps(output, cls=AnsibleJSONEncoder, indent=None, sort_keys=True))


    def _new_play(self, play):
        return {
            'meta': {
                'name': play.get_name(),
                'id': str(play._uuid),
                'duration': {'start': current_time()}
            },
            'tasks': []
        }


    def _new_task(self, task):
        return {
            'meta': {
                'name': task.get_name(),
                'id': str(task._uuid),
                'duration': {'start': current_time()}
            }
        }


    def _record_task_result(self, on_info, result, **kwargs):
        """This function is used as a partial to add failed/skipped info in a single method"""
        host = result._host
        task = result._task
        task_result = result._result.copy()

        # do not show ansible facts ; facts often exceed max line length
        if 'ansible_facts' in task_result:
            task_result['ansible_facts'] = {}

        task_result.update(on_info)
        task_result['action'] = task.action
        self.results[-1]['tasks'][-1].update(task_result)

        end_time = current_time()
        self.results[-1]['tasks'][-1]['meta']['duration']['end'] = end_time


        self.results[-1]['meta']['duration']['end'] = end_time

        output = self.results[-1]['tasks'][-1]
        # todo: figure out import error
        # v2_runner_on_ok: module 'ansible.plugins.callback.json' has no attribute 'dumps'
        self._display.display(dumps(output, cls=AnsibleJSONEncoder, indent=None, sort_keys=True))
