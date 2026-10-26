from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>BLACK WOLF IPTV DZ 🐺</title>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #000000; color: #22c55e; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 10px; }
        
        h1 { color: #22c55e; font-size: 20px; font-weight: bold; text-align: center; text-shadow: 0 0 10px rgba(34,197,94,0.5); margin-bottom: 5px; }
        .subtitle { font-size: 11px; color: #94a3b8; text-align: center; margin-bottom: 12px; }

        .player-container { width: 100%; max-width: 600px; background: #0b0f19; border: 2px solid #22c55e; border-radius: 12px; padding: 8px; margin-bottom: 12px; box-shadow: 0 0 20px rgba(34,197,94,0.3); }
        video { width: 100%; aspect-ratio: 16/9; display: block; background: #000; border-radius: 8px; transition: transform 0.3s ease; }

        .controls-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; width: 100%; max-width: 600px; margin-bottom: 10px; }
        .control-btn { background: #0b0f19; color: #22c55e; border: 2px solid #22c55e; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 12px; cursor: pointer; text-align: center; transition: 0.2s; }
        .control-btn:hover { background: #22c55e; color: #000; }

        .action-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; width: 100%; max-width: 600px; margin-bottom: 10px; }
        .action-select { background: #0b0f19; color: #22c55e; border: 2px solid #22c55e; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 12px; text-align: center; outline: none; cursor: pointer; }

        .countries-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; width: 100%; max-width: 600px; margin-bottom: 10px; }
        .country-btn { background: #0b0f19; color: #eab308; border: 1px solid #eab308; padding: 8px 4px; border-radius: 6px; font-weight: bold; font-size: 11px; cursor: pointer; text-align: center; transition: 0.2s; }
        .country-btn:hover, .country-btn.active { background: #eab308; color: #000; }

        .now-playing { width: 100%; max-width: 600px; font-size: 12px; color: #60a5fa; text-align: center; margin-bottom: 10px; background: #0b0f19; border: 1px solid #3b82f6; padding: 8px; border-radius: 6px; }

        .search-container { width: 100%; max-width: 600px; margin-bottom: 10px; }
        .search-input { width: 100%; padding: 12px; background: #0b0f19; border: 2px solid #22c55e; border-radius: 8px; color: #fff; font-size: 12px; outline: none; text-align: right; }
        .search-input::placeholder { color: #64748b; }

        .stats-card { width: 100%; max-width: 600px; background: #0b0f19; border: 2px solid #eab308; border-radius: 8px; padding: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; color: #eab308; font-weight: bold; font-size: 13px; }

        .channels-list { width: 100%; max-width: 600px; display: flex; flex-direction: column; gap: 8px; max-height: 45vh; overflow-y: auto; padding-right: 4px; }
        .channel-item { background: #0b0f19; border: 1px solid #22c55e; border-radius: 8px; padding: 10px 12px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: 0.2s; }
        .channel-item:hover { background: #111827; border-color: #4ade80; }
        .ch-name { font-weight: bold; font-size: 12px; color: #f8fafc; }
    </style>
</head>
<body>

    <h1>BLACK WOLF IPTV DZ 🐺</h1>
    <div class="subtitle">🇩🇿 شبكة السيطرة السحابية الشاملة لكل قنوات العالم</div>

    <div class="player-container">
        <video id="videoPlayer" controls autoplay playsinline></video>
    </div>

    <div class="controls-grid">
        <button class="control-btn" onclick="zoomVideo('out')">تصغير 🔽</button>
        <button class="control-btn" onclick="zoomVideo('reset')">عادي 🟦</button>
        <button class="control-btn" onclick="zoomVideo('in')">تكبير 🔼</button>
    </div>

    <div class="action-row">
        <button class="control-btn" onclick="toggleFullScreen()" style="width:100%;">شاشة كاملة 🔲</button>
        <select class="action-select" id="qualitySelect">
            <option value="auto">الدقة: تلقائي</option>
            <option value="720p">720p HD</option>
            <option value="1080p">1080p FHD</option>
        </select>
    </div>

    <div class="countries-grid">
        <button class="country-btn active" onclick="loadPlaylist('https://iptv-org.github.io/iptv/index.m3u', this)">🌍 كل العالم</button>
        <button class="country-btn" onclick="loadPlaylist('https://iptv-org.github.io/iptv/countries/dz.m3u', this)">🇩🇿 الجزائر</button>
        <button class="country-btn" onclick="loadPlaylist('https://iptv-org.github.io/iptv/countries/us.m3u', this)">🇺🇸 أمريكا</button>
        <button class="country-btn" onclick="loadPlaylist('https://iptv-org.github.io/iptv/countries/fr.m3u', this)">🇫🇷 فرنسا</button>
        <button class="country-btn" onclick="loadPlaylist('https://iptv-org.github.io/iptv/countries/ru.m3u', this)">🇷🇺 روسيا</button>
        <button class="country-btn" onclick="loadPlaylist('https://iptv-org.github.io/iptv/index.groups.m3u', this)">🌐 التصنيفات</button>
    </div>

    <div class="now-playing" id="nowPlayingText">▶ جاري التشغيل: اختر قناة للبدء</div>

    <div class="search-container">
        <input type="text" id="searchInput" class="search-input" placeholder="ابحث في آلاف القنوات الحقيقية..." onkeyup="filterChannels()">
    </div>

    <div class="stats-card">
        <span>القنوات الخاضعة للسيطرة:</span>
        <span id="totalCount">0 قناة</span>
    </div>

    <div class="channels-list" id="channelList">
        <div style="text-align:center; padding:20px; color:#22c55e;">📡 جاري جلب وسحب القنوات السحابية...</div>
    </div>

    <script>
        let allChannels = [];
        let displayedChannels = [];
        let hls = null;
        let currentScale = 1;

        async function loadPlaylist(url, btn) {
            if(btn) {
                document.querySelectorAll('.country-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }

            document.getElementById('channelList').innerHTML = '<div style="text-align:center; padding:20px; color:#eab308;">⏳ جاري سحب وتحميل القنوات بدقة عالية...</div>';
            
            try {
                const response = await fetch(url);
                const data = await response.text();
                parseM3U(data);
            } catch (error) {
                document.getElementById('channelList').innerHTML = '<div style="text-align:center; color:#ef4444; padding:15px;">⚠ تعذر الاتصال بالمصدر، تحقق من الإنترنت</div>';
            }
        }

        function parseM3U(m3uContent) {
            const lines = m3uContent.split('\\n');
            let list = [];
            let currentName = "قناة عالمية";

            for (let i = 0; i < lines.length; i++) {
                let line = lines[i].trim();
                if (line.startsWith('#EXTINF:')) {
                    let commaIdx = line.lastIndexOf(',');
                    if (commaIdx !== -1) {
                        currentName = line.substring(commaIdx + 1).trim();
                    }
                } else if (line && !line.startsWith('#') && (line.startsWith('http://') || line.startsWith('https://'))) {
                    list.push({ name: currentName, url: line });
                    currentName = "قناة عالمية";
                }
            }

            allChannels = list;
            displayedChannels = allChannels;
            document.getElementById('totalCount').innerText = allChannels.length + " قناة";
            renderList(displayedChannels);
        }

        function renderList(list) {
            const container = document.getElementById('channelList');
            container.innerHTML = '';
            
            if (list.length === 0) {
                container.innerHTML = '<div style="text-align:center; padding:20px; color:#ef4444;">لا توجد قنوات مطابقة للبحث</div>';
                return;
            }

            const fragment = document.createDocumentFragment();
            list.slice(0, 1000).forEach(ch => {
                const div = document.createElement('div');
                div.className = 'channel-item';
                div.innerHTML = `<span class="ch-name">📺 ${ch.name}</span><span>▶</span>`;
                div.onclick = () => playChannel(ch);
                fragment.appendChild(div);
            });
            container.appendChild(fragment);
        }

        function playChannel(ch) {
            document.getElementById('nowPlayingText').innerText = `▶ جاري تشغيل: ${ch.name}`;
            const video = document.getElementById('videoPlayer');
            
            if (hls) {
                hls.destroy();
                hls = null;
            }

            if (Hls.isSupported() && ch.url.includes('.m3u8')) {
                hls = new Hls();
                hls.loadSource(ch.url);
                hls.attachMedia(video);
                hls.on(Hls.Events.MANIFEST_PARSED, () => {
                    video.play().catch(e => console.log("Autoplay restricted"));
                });
            } else {
                video.src = ch.url;
                video.play().catch(e => {
                    document.getElementById('nowPlayingText').innerText = `⚠ الرابط يتطلب مشغل خارجي`;
                });
            }
        }

        function zoomVideo(type) {
            const video = document.getElementById('videoPlayer');
            if (type === 'in') currentScale += 0.1;
            else if (type === 'out') currentScale = Math.max(0.8, currentScale - 0.1);
            else currentScale = 1;
            video.style.transform = `scale(${currentScale})`;
        }

        function toggleFullScreen() {
            const video = document.getElementById('videoPlayer');
            if (video.requestFullscreen) video.requestFullscreen();
        }

        function filterChannels() {
            const q = document.getElementById('searchInput').value.toLowerCase();
            if (!q) {
                renderList(allChannels);
                document.getElementById('totalCount').innerText = allChannels.length + " قناة";
                return;
            }
            const filtered = allChannels.filter(c => c.name.toLowerCase().includes(q));
            renderList(filtered);
            document.getElementById('totalCount').innerText = filtered.length + " قناة مطابقة";
        }

        loadPlaylist('https://iptv-org.github.io/iptv/index.m3u');
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


