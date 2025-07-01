function RegisterMainInput() {
  const user_id = document.getElementById('reg-id').value;
  const stu_pass = document.getElementById('reg-pass').value;
  const stu_pass2 = document.getElementById('reg-confirm').value;
  const error = document.getElementById('reg-error');

  if (!/^\d{5}$/.test(user_id)) {
    error.textContent = '学籍番号は5桁の半角数字です';
    return;
  }

  if (!/^[0-9A-Za-z]{8,64}$/.test(stu_pass)) {
    error.textContent = 'パスワードは8文字以上64文字以下の半角英数字です';
    return;
  }

  if (stu_pass !== stu_pass2) {
    error.textContent = 'パスワードが一致しません';
    return;
  }

  // 仮登録成功
  alert("登録完了。ログイン画面へ遷移");
  window.location.href = 'Login.html';
}
