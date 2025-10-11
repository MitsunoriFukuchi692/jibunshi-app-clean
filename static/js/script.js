document.getElementById("generateBtn").addEventListener("click", async () => {
  const prompt = document.getElementById("prompt").value.trim();
  const resultDiv = document.getElementById("result");
  if (!prompt) { resultDiv.textContent = "入力してください。"; return; }
  resultDiv.textContent = "生成中です…⏳";
  try {
    const r = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });
    const data = await r.json();
    if (data.result) resultDiv.textContent = data.result;
    else resultDiv.textContent = data.error || "不明なエラーです。";
  } catch (e) {
    resultDiv.textContent = "通信エラー: " + e;
  }
});
