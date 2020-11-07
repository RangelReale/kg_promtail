from kubragen.configfile import ConfigFileExtension, ConfigFile, ConfigFileExtensionData
from kubragen.options import OptionGetter


class PromtailConfigFileExt_Kubernetes(ConfigFileExtension):
    """
    Promtail configuration extension for Kubernetes scrape config.
    """
    def process(self, configfile: ConfigFile, data: ConfigFileExtensionData, options: OptionGetter) -> None:
        if 'scrape_configs' not in data.data:
            data.data['scrape_configs'] = []
        data.data['scrape_configs'].extend([{
            'job_name': 'kubernetes-pods-name',
            'pipeline_stages': [{'docker': {}}],
            'kubernetes_sd_configs': [{'role': 'pod'}],
            'relabel_configs': [{
                'source_labels': ['__meta_kubernetes_pod_label_name'],
                'target_label': '__service__'
            },
            {
                'source_labels': ['__meta_kubernetes_pod_node_name'],
                'target_label': '__host__'
            },
            {
                'action': 'drop',
                'regex': '',
                'source_labels': ['__service__']
            },
            {
                'action': 'labelmap',
                'regex': '__meta_kubernetes_pod_label_(.+)'
            },
            {
                'action': 'replace',
                'replacement': '$1',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_namespace', '__service__'],
                'target_label': 'job'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_namespace'],
                'target_label': 'namespace'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_name'],
                'target_label': 'pod'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_container_name'],
                'target_label': 'container'
            },
            {
                'replacement': '/var/log/pods/*$1/*.log',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_pod_uid', '__meta_kubernetes_pod_container_name'],
                'target_label': '__path__'
            }]
        },
        {
            'job_name': 'kubernetes-pods-app',
            'pipeline_stages': [{'docker': {}}],
            'kubernetes_sd_configs': [{'role': 'pod'}],
            'relabel_configs': [{
                'action': 'drop',
                'regex': '.+',
                'source_labels': ['__meta_kubernetes_pod_label_name']
            },
            {
                'source_labels': ['__meta_kubernetes_pod_label_app'],
                'target_label': '__service__'
            },
            {
                'source_labels': ['__meta_kubernetes_pod_node_name'],
                'target_label': '__host__'
            },
            {
                'action': 'drop',
                'regex': '',
                'source_labels': ['__service__']
            },
            {
                'action': 'labelmap',
                'regex': '__meta_kubernetes_pod_label_(.+)'
            },
            {
                'action': 'replace',
                'replacement': '$1',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_namespace',
                    '__service__'],
                'target_label': 'job'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_namespace'],
                'target_label': 'namespace'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_name'],
                'target_label': 'pod'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_container_name'],
                'target_label': 'container'
            },
            {
                'replacement': '/var/log/pods/*$1/*.log',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_pod_uid',
                    '__meta_kubernetes_pod_container_name'],
                'target_label': '__path__'
            }]
        },
        {
            'job_name': 'kubernetes-pods-direct-controllers',
            'pipeline_stages': [{'docker': {}}],
            'kubernetes_sd_configs': [{'role': 'pod'}],
            'relabel_configs': [{
                'action': 'drop',
                'regex': '.+',
                'separator': '',
                'source_labels': ['__meta_kubernetes_pod_label_name', '__meta_kubernetes_pod_label_app']
            },
            {
                'action': 'drop',
                'regex': '[0-9a-z-.]+-[0-9a-f]{8,10}',
                'source_labels': ['__meta_kubernetes_pod_controller_name']
            },
            {
                'source_labels': ['__meta_kubernetes_pod_controller_name'],
                'target_label': '__service__'
            },
            {
                'source_labels': ['__meta_kubernetes_pod_node_name'],
                'target_label': '__host__'
            },
            {
                'action': 'drop',
                'regex': '',
                'source_labels': ['__service__']
            },
            {
                'action': 'labelmap',
                'regex': '__meta_kubernetes_pod_label_(.+)'
            },
            {
                'action': 'replace',
                'replacement': '$1',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_namespace',
                    '__service__'],
                'target_label': 'job'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_namespace'],
                'target_label': 'namespace'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_name'],
                'target_label': 'pod'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_container_name'],
                'target_label': 'container'
            },
            {
                'replacement': '/var/log/pods/*$1/*.log',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_pod_uid',
                    '__meta_kubernetes_pod_container_name'],
                'target_label': '__path__'
            }]
        },
        {
            'job_name': 'kubernetes-pods-indirect-controller',
            'pipeline_stages': [{'docker': {}}],
            'kubernetes_sd_configs': [{'role': 'pod'}],
            'relabel_configs': [{
                'action': 'drop',
                'regex': '.+',
                'separator': '',
                'source_labels': ['__meta_kubernetes_pod_label_name',
                    '__meta_kubernetes_pod_label_app']
            },
            {
                'action': 'keep',
                'regex': '[0-9a-z-.]+-[0-9a-f]{8,10}',
                'source_labels': ['__meta_kubernetes_pod_controller_name']
            },
            {
                'action': 'replace',
                'regex': '([0-9a-z-.]+)-[0-9a-f]{8,10}',
                'source_labels': ['__meta_kubernetes_pod_controller_name'],
                'target_label': '__service__'
            },
            {
                'source_labels': ['__meta_kubernetes_pod_node_name'],
                'target_label': '__host__'
            },
            {
                'action': 'drop',
                'regex': '',
                'source_labels': ['__service__']
            },
            {
                'action': 'labelmap',
                'regex': '__meta_kubernetes_pod_label_(.+)'
            },
            {
                'action': 'replace',
                'replacement': '$1',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_namespace',
                    '__service__'],
                'target_label': 'job'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_namespace'],
                'target_label': 'namespace'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_name'],
                'target_label': 'pod'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_container_name'],
                'target_label': 'container'
            },
            {
                'replacement': '/var/log/pods/*$1/*.log',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_pod_uid',
                    '__meta_kubernetes_pod_container_name'],
                'target_label': '__path__'
            }]
        },
        {
            'job_name': 'kubernetes-pods-static',
            'pipeline_stages': [{'docker': {}}],
            'kubernetes_sd_configs': [{'role': 'pod'}],
            'relabel_configs': [{
                'action': 'drop',
                'regex': '',
                'source_labels': ['__meta_kubernetes_pod_annotation_kubernetes_io_config_mirror']
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_label_component'],
                'target_label': '__service__'
            },
            {
                'source_labels': ['__meta_kubernetes_pod_node_name'],
                'target_label': '__host__'
            },
            {
                'action': 'drop',
                'regex': '',
                'source_labels': ['__service__']
            },
            {
                'action': 'labelmap',
                'regex': '__meta_kubernetes_pod_label_(.+)'
            },
            {
                'action': 'replace',
                'replacement': '$1',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_namespace',
                    '__service__'],
                'target_label': 'job'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_namespace'],
                'target_label': 'namespace'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_name'],
                'target_label': 'pod'
            },
            {
                'action': 'replace',
                'source_labels': ['__meta_kubernetes_pod_container_name'],
                'target_label': 'container'
            },
            {
                'replacement': '/var/log/pods/*$1/*.log',
                'separator': '/',
                'source_labels': ['__meta_kubernetes_pod_annotation_kubernetes_io_config_mirror',
                    '__meta_kubernetes_pod_container_name'],
                'target_label': '__path__'
            }],
        }])