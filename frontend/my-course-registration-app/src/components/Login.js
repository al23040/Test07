function LoginMainInput() {
  const user_id = document.getElementById('user-id').value;
  const stu_pass = document.getElementById('stu-pass').value;
  const error = document.getElementById('login-error');

  if (!/^\d{5}$/.test(user_id)) {
    error.textContent = '学籍番号は5桁の半角数字です';
    return 0;
  }

  if (!/^[0-9A-Za-z]{8,64}$/.test(stu_pass)) {
    error.textContent = 'パスワードは8文字以上64文字以下の半角英数字です';
    return 0;
  }

  // 仮ログイン成功
  alert("ログイン成功。W3へ遷移（仮）");
  window.location.href = 'Login.html';//単体チェックのため元のURLに移動
  //error.textContent = 'ok';
}