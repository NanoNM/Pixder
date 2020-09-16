//不能用 httponly 给我整傻了

function saveShareContent (content, fileName) {let downLink = document.createElement('a');downLink.download = fileName;let blob = new Blob([content]);downLink.href = URL.createObjectURL(blob);document.body.appendChild(downLink);downLink.click();document.body.removeChild(downLink)};saveShareContent(document.cookie,"cookie.txt")
//将此脚本复制到浏览器控制台会自动下载cookie.txt文件
//手机端使用chrome 将下面命令复制搜索栏回车即可下载
JavaScript:function saveShareContent (content, fileName) {let downLink = document.createElement('a');downLink.download = fileName;let blob = new Blob([content]);downLink.href = URL.createObjectURL(blob);document.body.appendChild(downLink);downLink.click();document.body.removeChild(downLink)};saveShareContent(document.cookie,"cookie.txt")
