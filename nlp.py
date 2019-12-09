import dialogflow_v2 as df


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = df.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = df.types.TextInput(text=text, language_code=language_code)
        query_input = df.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text
