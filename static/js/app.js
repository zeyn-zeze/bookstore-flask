
function enableEdit(userId) {
    const row = document.getElementById('row_' + userId);
    const updateBtn = document.getElementById('update_btn_' + userId);
    const saveBtn = document.getElementById('save_btn_' + userId);

    const texts = row.querySelectorAll('.text');
    const edits = row.querySelectorAll('.edit');

    texts.forEach(t => t.style.display = 'none');
    edits.forEach(e => e.style.display = 'inline-block');

    updateBtn.style.display = 'none';
    saveBtn.style.display = 'inline-block';
}



function confirmDelete() {
    return confirm('Are you sure you want to delete this user?');
}
