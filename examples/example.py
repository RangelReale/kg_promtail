from kubragen import KubraGen
from kubragen.consts import PROVIDER_GOOGLE, PROVIDERSVC_GOOGLE_GKE
from kubragen.object import Object
from kubragen.option import OptionRoot
from kubragen.options import Options
from kubragen.output import OutputProject, OD_FileTemplate, OutputFile_ShellScript, OutputFile_Kubernetes, \
    OutputDriver_Print
from kubragen.provider import Provider

from kg_promtail import PromtailBuilder, PromtailOptions, PromtailConfigFile, PromtailConfigFileOptions, \
    PromtailConfigFileExt_Kubernetes

kg = KubraGen(provider=Provider(PROVIDER_GOOGLE, PROVIDERSVC_GOOGLE_GKE), options=Options({
    'namespaces': {
        'mon': 'app-monitoring',
    },
}))

out = OutputProject(kg)

shell_script = OutputFile_ShellScript('create_gke.sh')
out.append(shell_script)

shell_script.append('set -e')

#
# OUTPUTFILE: app-namespace.yaml
#
file = OutputFile_Kubernetes('app-namespace.yaml')

file.append([
    Object({
        'apiVersion': 'v1',
        'kind': 'Namespace',
        'metadata': {
            'name': 'app-monitoring',
        },
    }, name='ns-monitoring', source='app', instance='app')
])

out.append(file)
shell_script.append(OD_FileTemplate(f'kubectl apply -f ${{FILE_{file.fileid}}}'))

shell_script.append(f'kubectl config set-context --current --namespace=app-monitoring')

#
# SETUP: promtail
#
promtailconfigfile = PromtailConfigFile(options=PromtailConfigFileOptions({
}), extensions=[PromtailConfigFileExt_Kubernetes()])

promtail_config = PromtailBuilder(kubragen=kg, options=PromtailOptions({
    'namespace': OptionRoot('namespaces.mon'),
    'basename': 'mypromtail',
    'config': {
        'promtail_config': promtailconfigfile,
        'loki_url': 'http://loki:3100',
    },
    'kubernetes': {
        'resources': {
            'daemonset': {
                'requests': {
                    'cpu': '150m',
                    'memory': '300Mi'
                },
                'limits': {
                    'cpu': '300m',
                    'memory': '450Mi'
                },
            },
        },
    }
}))

promtail_config.ensure_build_names(promtail_config.BUILD_ACCESSCONTROL, promtail_config.BUILD_CONFIG,
                                   promtail_config.BUILD_SERVICE)

#
# OUTPUTFILE: promtail-config.yaml
#
file = OutputFile_Kubernetes('promtail-config.yaml')
out.append(file)

file.append(promtail_config.build(promtail_config.BUILD_ACCESSCONTROL, promtail_config.BUILD_CONFIG))

shell_script.append(OD_FileTemplate(f'kubectl apply -f ${{FILE_{file.fileid}}}'))

#
# OUTPUTFILE: promtail.yaml
#
file = OutputFile_Kubernetes('promtail.yaml')
out.append(file)

file.append(promtail_config.build(promtail_config.BUILD_SERVICE))

shell_script.append(OD_FileTemplate(f'kubectl apply -f ${{FILE_{file.fileid}}}'))

#
# Write files
#
out.output(OutputDriver_Print())
# out.output(OutputDriver_Directory('/tmp/build-gke'))
