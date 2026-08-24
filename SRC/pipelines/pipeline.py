from SRC.agents.agants import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:

    state = {}

    # search agent working
    print("\n" + "=" * 50)
    print("step 1 - search is working ...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "input": f"Find recent, reliable and detailed information about {topic}"
    })
    state["search_results"] = search_result["output"]
                    


    # reader agent
    print("\n" + "=" * 50)
    print("step 2 - reader agent is working ...")
    print("=" * 50)

    read_agent = build_reader_agent()
    reader_result = read_agent.invoke({
        "input": f"Based on the following search results about {topic} "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f" Search Results :\n{state['search_results'][:800]}"
    })
    state["scraped_content"] = reader_result["output"]




    # writer agent
    print("\n" + "=" * 50)
    print("step 3 - writer agent is working ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT :\n {state['scraped_content']}"
  )
    state["report"] = writer_chain.invoke({
        "topic" : topic,
        'research' : research_combined
    })

    print("\n Final Report\n", state["report"])


    
    # critic report
    print("\n" + "=" * 50)
    print("step 3 - critic report is working ...")
    print("=" * 50)
    

    state["feedback"] = critic_chain.invoke({
        "report" : state["report"]
    })

    print("\n Critic Report\n", state["feedback"])

    return state