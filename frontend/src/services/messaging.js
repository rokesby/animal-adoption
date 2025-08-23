export const getConversations = async (authFetch) => {

    const response = await authFetch('/api/conversations',  {method: "GET"});
    if (response.status !== 200) {
        console.log(response)
        if (response.status == 403) {
            console.log("manual error: response 403")
        } else {
            throw new Error("Unable to fetch messages")
        }
    }

    const responseData = await response.json();
    return responseData;
}

export const getConversationsMessages = async (authFetch, id) => {

    const response = await authFetch(`/api/conversations/${id}/messages`,  {method: "GET"});
    if (response.status !== 200) {
        console.log(response)
        if (response.status == 403) {
            console.log("manual error: response 403")
        } else {
            throw new Error("Unable to fetch messages")
        }
    }

    const responseData = await response.json();
    return responseData;
}

export const replyToConversationMessages = async (authFetch, formData, id) => {
    const requestOptions = {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
        credentials: "include",
    };
    console.log('id', id)
    const response = await authFetch(`/api/conversations/${id}/messages`,  requestOptions);

    if (response.status != 201) {
        if (response.status == 403) {
            throw new Error('Error:', response['error'])
        } else {
            throw new Error('Unable to send message')
        }
    }

    const responseData = response.json()
    console.log(responseData)
    return responseData
}