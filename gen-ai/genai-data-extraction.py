import oci
# Setup basic variables
# Auth Config
# TODO: Please update config profile name and use the compartmentId that has policies grant permissions for using Generative AI Service
compartment_id = "<COMPARTMENT_ID>"
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('.oci/config', CONFIG_PROFILE)
# Service endpoint
endpoint = "<ENDPOINT_ID>"
generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
chat_detail = oci.generative_ai_inference.models.ChatDetails()
chat_request = oci.generative_ai_inference.models.CohereChatRequest()
chat_request.max_tokens = 600
chat_request.temperature = 0.05  #.25
chat_request.frequency_penalty = 0
chat_request.top_p = 0.8  #.75
chat_request.top_k = 0
chat_detail.compartment_id = compartment_id
chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="<MODEL_ID>")
######
object_storage_client = oci.object_storage.ObjectStorageClient(config=config)
training_data = "/u01/PPA_TOP/.oci/preamble.txt"
#chat_instruction = "Please analyze below patch instruction and tell us Code levels, Command & Prerequisite:\n"
#######
with open(training_data, "r") as file:
    chat_request.preamble_override=file.read()
patch_num = input("Enter patch# to analyze the Readme file:\n")
'''file_path = '<FILE_ORDER>' + patch_num + '/README.txt'
# Upload the file
print("Step 1: Attempting to upload the README File ...")
with open(file_path, "rb") as f:
    print("Got README File ...")
    object_storage_client.put_object(namespace_name='omcsmig',
                                     bucket_name='<BUCKET_NAME>',
                                     object_name="PPA_GenAI/{}/README.txt".format(patch_num), put_object_body=f)
print("        README File uploaded successfully!")'''
print("Step 1: Getting Readme file content from the Object Storage...")
get_object_response = object_storage_client.get_object(namespace_name='<NAMESPACE_ID>',
                                                       bucket_name='<BUCKET_NAME>',
                                                       object_name=f"PySdkTest/README_{patch_num}.txt")
#print(str(get_object_response.data.content.decode()))
print("        Loacated README File successfully!")
#######
#chat_request.message = chat_instruction + content
#chat_request.message = chat_instruction + str(get_object_response.data.content.decode())
chat_request.message = str(get_object_response.data.content.decode())
chat_detail.chat_request = chat_request
print("Step 2: GenAI LLM chat analyzing the Readme file...")
chat_response = generative_ai_inference_client.chat(chat_detail)
chat_data=vars(chat_response)['data']
print("        GenAI LLM chat analyzed the Readme file")
# Store output to Object Storage
print("Step 3: Saving GenAI LLM chat response ...")
save_response = object_storage_client.put_object(namespace_name='<NAMESPACE_ID>',
                                                 bucket_name='<BUCKET_NAME>',
                                                 object_name="PPA_GenAI/{}/pre_patch_analysis.txt".format(patch_num),
                                                 put_object_body = chat_data.chat_response.chat_history[1].message)
#print(str(save_response.data))
print("        Saved GenAI LLM chat response successfully")
# Print result
print("\n\n**************************Chat Result**************************")
print(chat_data.chat_response.chat_history[1].message)
print("****************************************************************")
