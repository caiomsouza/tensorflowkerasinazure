from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import InferenceConfig
from azureml.core import Model
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.webservice import AciWebservice, Webservice, LocalWebservice

sp = ServicePrincipalAuthentication(tenant_id="72f988bf-86f1-41af-91ab-2d7cd011db47", # tenantID
                                    service_principal_id="2faad9e6-8bf9-4e7d-a732-70e3daa5ffd5", # clientId
                                    service_principal_password="c536a902-db8f-4b3c-9774-bd9daf4bcc69") # clientSecret

# Create an environment and add conda dependencies to it
myenv = Environment(name="myenv")
# Enable Docker based environment
myenv.docker.enabled = True
# Build conda dependencies
myenv.python.conda_dependencies = CondaDependencies.create(conda_packages=['python==3.7.6','scikit-learn','tensorflow==2.1.0','pandas','numpy','matplotlib'],
                                                           pip_packages=['pillow','azureml-defaults','inference-schema[numpy-support]'])
inference_config = InferenceConfig(entry_script="score.py", environment=myenv, source_directory='packagefordeployment/')
ws = Workspace('bd04922c-a444-43dc-892f-74d5090f8a9a', 'mlplayarearg', 'testdeployment',auth=sp)

model = Model(workspace=ws, name='dogbreedclassifiernew')

deployment_config = AciWebservice.deploy_configuration(cpu_cores = 1, memory_gb = 3)
#deployment_config = LocalWebservice.deploy_configuration(port=8890)

service = Model.deploy(ws, "identiydogbreedv2", [model], inference_config, deployment_config, overwrite=True)
service.wait_for_deployment(show_output = True)
print(service.state)