// Store a reference to the original fetch function
window.originalFetch = window.fetch;

// Define a new fetch function that wraps the original fetch

window.fetch = async function (url, options) {
    try {
        // Call the original fetch function
        const response = await originalFetch(url, options);

        // Check if the response has a JSON content type
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            // If the response is JSON, clone the response so we can read it twice
            const responseClone = response.clone();
            // Parse the JSON data and save it to the fetchedData object
            const jsonData = await responseClone.json();
            // NOW: if url for https://chat.openai.com/backend-api/conversation/...
            // do something very special with it
            const pattern =
                /^https:\/\/chat\.openai\.com\/backend-api\/conversation\/(.*)/;
            const match = url.match(pattern);
            if (match) {
                const conversationId = match[1];
                console.log("conversationId", conversationId);
                console.log("jsonData", jsonData);
                const conversation = {
                    id: conversationId,
                    title: jsonData.title,
                    create_time: jsonData.create_time,
                    moderation_results: JSON.stringify(jsonData.moderation_results),
                    current_node: jsonData.current_node,
                    plugin_ids: JSON.stringify(jsonData.plugin_ids),
                };
                fetch(
                    "http://localhost:5000/chatgpt_conversation/-/insert",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        mode: "cors",
                        body: JSON.stringify({
                            row: conversation,
                            replace: true,
                        }),
                    }
                )
                    .then((d) => d.json())
                    .then((d) => console.log("d", d));
                const messages = Object.values(jsonData.mapping)
                    .filter((m) => m.message)
                    .map((message) => {
                        m = message.message;
                        let content = "";
                        if (m.content) {
                            if (m.content.text) {
                                content = m.content.text;
                            } else {
                                content = m.content.parts.join("\n");
                            }
                        }
                        return {
                            id: m.id,
                            conversation_id: conversationId,
                            author_role: m.author ? m.author.role : null,
                            author_metadata: JSON.stringify(
                                m.author ? m.author.metadata : {}
                            ),
                            create_time: m.create_time,
                            content: content,
                            end_turn: m.end_turn,
                            weight: m.weight,
                            metadata: JSON.stringify(m.metadata),
                            recipient: m.recipient,
                        };
                    });
                fetch(
                    "http://localhost:5000/chatgpt_message/-/insert",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        mode: "cors",
                        body: JSON.stringify({
                            rows: messages,
                            replace: true,
                        }),
                    }
                )
                    .then((d) => d.json())
                    .then((d) => console.log("d", d));
            }
        }

        // Return the original response
        return response;
    } catch (error) {
        // Handle any errors that occur during the fetch
        console.error("Error fetching and saving JSON:", error);
        throw error;
    }
};
