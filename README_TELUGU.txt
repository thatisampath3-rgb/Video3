SVSC AUTOMATIC VIDEO CREATOR PRO

ఇది Python + Flask ఆధారంగా పనిచేసే ప్రారంభ వెర్షన్.
సదుపాయాలు:
- స్క్రిప్ట్‌ను సీన్లుగా విడగొట్టి ఇవ్వవచ్చు (ప్రతి లైన్ ఒక సీన్)
- తెలుగు AI వాయిస్ (Shruti / Mohan)
- సీన్ ఇమేజెస్ upload చేయవచ్చు
- 9:16 Shorts/Reels లేదా 16:9 YouTube
- MP4 వీడియో డౌన్‌లోడ్

ఇన్‌స్టాలేషన్:
1. కంప్యూటర్‌లో Python 3.10 లేదా కొత్త వెర్షన్ ఇన్‌స్టాల్ చేయండి.
2. FFmpeg ఇన్‌స్టాల్ చేసి PATHలో చేర్చండి.
3. NotoSansTelugu-Regular.ttf ఫాంట్‌ను ఈ ఫోల్డర్‌లో ఉంచండి.
4. ఈ ఫోల్డర్‌లో Terminal / CMD ఓపెన్ చేయండి.
5. అమలు చేయండి:
   pip install -r requirements.txt
6. తరువాత:
   python app.py
7. Browserలో తెరవండి:
   http://127.0.0.1:5000

ముఖ్య గమనికలు:
- తెలుగు వాయిస్ తయారీకి internet అవసరం.
- ప్రతి కొత్త లైన్ ఒక సీన్‌గా పరిగణించబడుతుంది.
- ఇమేజెస్‌ను అదే సీన్ క్రమంలో upload చేయండి; లేని సీన్లకు plain background వస్తుంది.
- ఇది local development version. Public hostingకు upload చేయడానికి ముందు file-size limits,
  authentication, secure secret key, job queue, storage మరియు usage limits జోడించాలి.
- MP4 exportకు FFmpeg అవసరం.

MOBILE ONLINE DEPLOYMENT (Render):
ఈ ప్రాజెక్ట్‌ను Render వంటి Python hostingలో deploy చేసిన తర్వాత Android/iPhone browserలో URL ఓపెన్ చేసి ఉపయోగించవచ్చు.

1. ZIP extract చేయండి.
2. GitHubలో కొత్త repository సృష్టించి ఈ ఫోల్డర్‌లోని files upload చేయండి.
3. Render.comలో account సృష్టించి New > Blueprint ఎంచుకోండి.
4. GitHub repository connect చేయండి. render.yaml ద్వారా service setup అవుతుంది.
5. Deploy పూర్తయ్యాక Render ఇచ్చే https://....onrender.com URLను మొబైల్‌లో తెరవండి.

గమనిక:
- ఈ యాప్ Python backend అవసరం కాబట్టి కేవలం static hosting లేదా సాధారణ Vercel static deploymentలో నేరుగా పనిచేయదు.
- Free hostingలో service sleep కావచ్చు; మొదటి requestకు సమయం పట్టవచ్చు.
- Free instanceలో పెద్ద వీడియోలు/చాలా సీన్లు timeout లేదా memory సమస్య ఇవ్వవచ్చు.
- Free filesystem తాత్కాలికం; వీడియోను వెంటనే download చేసుకోండి.
- Production వినియోగానికి paid hosting, upload limits, login, job queue, persistent/object storage మరియు secure configuration అవసరం.
