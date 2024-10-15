const targetDiv = document.querySelector('.x78zum5.xdt5ytf.x1iyjqo2');

if (targetDiv){const content = targetDiv.outerHTML; console.log(content);
navigator.clipboard.writeText(content).then(() => { console.log("content copied to clipboard");}).catch(err => {console.error('failed to copy', err); }); } else { console.error("div not found"); }
