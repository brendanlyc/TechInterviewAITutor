export const handleFormSubmit = async({
    e,
    apiUrl,
    method = 'POST',
    headers = {'Content-Type': 'application/json'},
    body,
    onSuccess,
    onError
}) => {
    e.preventDefault();

    try {
        console.log(apiUrl)
        const response = await fetch(apiUrl, {
            method,
            headers,
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Something went wrong");
        }

        const data = await response.json();

        if (onSuccess) {
            onSuccess(data);
        }
    } catch (err) {
        console.error(err);
        if (onError) {
            onError(err.message);
        }
    }
};