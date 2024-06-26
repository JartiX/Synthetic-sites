document.addEventListener('DOMContentLoaded', () => {
    const handleFormSubmit = async (e, method, endpoint) => {
        e.preventDefault();
        const formData = new FormData(e.target);

        formData.append('API-KEY', apiKey);
        
        const params = new URLSearchParams(formData)
        
        try {
            const response = await axios({
                method: method,
                url: endpoint,
                params: params
            });
            data = response.data
            if (response.status === 200) {
                console.log(data);

                alert(`Success: ${JSON.stringify(data)}`);
            }
            else {
                alert(`Error: ${JSON.stringify(data)}`)
            }
        }
        catch (error) {
            alert('Error: ' + error.message);
        }
    };

    // Attach event listeners to each form
    document.getElementById('removeUserForm').addEventListener('submit', (e) => handleFormSubmit(e, 'DELETE', '/api/remove_user_by_id'));
    document.getElementById('createUserForm').addEventListener('submit', (e) => handleFormSubmit(e, 'POST', '/api/create_user'));
    document.getElementById('makeAdminForm').addEventListener('submit', (e) => handleFormSubmit(e, 'PUT', '/api/make_admin_by_id'));
    document.getElementById('getUsernameForm').addEventListener('submit', (e) => handleFormSubmit(e, 'GET', '/api/get_username_by_id'));
    document.getElementById('getEmailForm').addEventListener('submit', (e) => handleFormSubmit(e, 'GET', '/api/get_email_by_id'));
    document.getElementById('getIdByUsernameForm').addEventListener('submit', (e) => handleFormSubmit(e, 'GET', '/api/get_id_by_username'));
    document.getElementById('getIdByEmailForm').addEventListener('submit', (e) => handleFormSubmit(e, 'GET', '/api/get_id_by_email'));
    document.getElementById('deleteSiteFromMainPageForm').addEventListener('submit', (e) => handleFormSubmit(e, 'DELETE', '/api/delete_site_from_main_page'));
    document.getElementById('addExistedSiteForm').addEventListener('submit', (e) => handleFormSubmit(e, 'POST', '/api/add_existed_site'));
    document.getElementById('deleteSiteForm').addEventListener('submit', (e) => handleFormSubmit(e, 'DELETE', '/api/delete_site'));
    document.getElementById('createSiteForm').addEventListener('submit', (e) => handleFormSubmit(e, 'POST', '/api/create_site'));
    document.getElementById('getUsersForm').addEventListener('submit', (e) => handleFormSubmit(e, 'GET', '/api/get_users'));
});
