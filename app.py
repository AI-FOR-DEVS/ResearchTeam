import autogen
from search import search, search_declaration
from prompts import websearcher, reporter, critic, manager

llm_config = {"config_list": autogen.config_list_from_json("OAI_CONFIG_LIST")}

websearcher = autogen.AssistantAgent(
    name="websearcher",
    llm_config={"config_list": autogen.config_list_from_json("OAI_CONFIG_LIST"), "functions": [search_declaration]},
    system_message=websearcher
)

reporter = autogen.AssistantAgent(
    name="reporter",
    llm_config=llm_config,
    system_message=reporter
)

critic = autogen.AssistantAgent(
    name="critic",
    llm_config=llm_config,
    system_message=critic
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    system_message="""
     Reply TERMINATE if the task has been solved at full satisfaction.
     Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

groupchat = autogen.GroupChat(
    agents=[websearcher, reporter, critic, user_proxy], messages=[]
)

manager = autogen.GroupChatManager(
    llm_config=llm_config, groupchat=groupchat, system_message=manager
)

user_proxy.initiate_chat(
    manager, message="What are the main disadvantages for startups in Germany?"
)
