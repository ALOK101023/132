import { useState, useEffect, useRef } from "react";

/* ══════════════════════════════════════════════════════════════
   MAJDOOR ADHIKAAR SAHAYAK — Visual Redesign
   Aesthetic: Warm Indian Editorial × Modern Glassmorphism
   Palette: Deep Indigo + Saffron + Cream + Earth tones
   ══════════════════════════════════════════════════════════════ */

const HELPLINES = [
  { name: "श्रम हेल्पलाइन", number: "14434", desc: "केंद्र सरकार श्रम शिकायत", icon: "⚖️" },
  { name: "महिला हेल्पलाइन", number: "181", desc: "महिला श्रमिकों के लिए", icon: "👩" },
  { name: "चाइल्ड लेबर", number: "1098", desc: "बाल श्रम शिकायत", icon: "👶" },
  { name: "पुलिस", number: "100", desc: "आपातकालीन स्थिति", icon: "🚔" },
  { name: "EPFO हेल्पलाइन", number: "1800-118-005", desc: "PF संबंधित शिकायत", icon: "🏦" },
  { name: "ESIC हेल्पलाइन", number: "1800-11-2526", desc: "बीमा संबंधित शिकायत", icon: "🏥" },
];

const ISSUE_TYPES = [
  { id: "wage", label: "वेतन नहीं मिला", icon: "💰", law: "Payment of Wages Act, 1936" },
  { id: "overtime", label: "ओवरटाइम नहीं दिया", icon: "⏰", law: "Factories Act, 1948 - Section 59" },
  { id: "fired", label: "बिना नोटिस निकाला", icon: "🚪", law: "Industrial Disputes Act, 1947" },
  { id: "unsafe", label: "असुरक्षित कार्यस्थल", icon: "⚠️", law: "Factories Act, 1948" },
  { id: "harassment", label: "उत्पीड़न / शोषण", icon: "🛡️", law: "POSH Act, 2013" },
  { id: "child", label: "बाल श्रम", icon: "👶", law: "Child Labour Act, 1986" },
  { id: "bonded", label: "बंधुआ मजदूरी", icon: "⛓️", law: "Bonded Labour Act, 1976" },
  { id: "pf", label: "PF / ESI नहीं काटा", icon: "🏦", law: "EPF Act, 1952" },
  { id: "other", label: "अन्य समस्या", icon: "📋", law: "" },
];

const STATES = {
  "दिल्ली": { office: "श्रम आयुक्त कार्यालय, 5 शाम नाथ मार्ग", phone: "011-23962406" },
  "उत्तर प्रदेश": { office: "श्रम आयुक्त कार्यालय, लखनऊ", phone: "0522-2238218" },
  "मध्य प्रदेश": { office: "श्रम आयुक्त कार्यालय, भोपाल", phone: "0755-2551399" },
  "महाराष्ट्र": { office: "श्रम आयुक्त कार्यालय, मुंबई", phone: "022-24934091" },
  "राजस्थान": { office: "श्रम आयुक्त कार्यालय, जयपुर", phone: "0141-2227810" },
  "बिहार": { office: "श्रम आयुक्त कार्यालय, पटना", phone: "0612-2504810" },
  "हरियाणा": { office: "श्रम आयुक्त कार्यालय, चंडीगढ़", phone: "0172-2701373" },
  "गुजरात": { office: "श्रम आयुक्त कार्यालय, अहमदाबाद", phone: "079-25506789" },
  "तमिलनाडु": { office: "श्रम आयुक्त कार्यालय, चेन्नई", phone: "044-25671067" },
  "पंजाब": { office: "श्रम आयुक्त कार्यालय, चंडीगढ़", phone: "0172-2744011" },
};

const QUIZ = [
  { q: "न्यूनतम वेतन कौन तय करता है?", o: ["मालिक", "सरकार", "कोर्ट", "पुलिस"], c: 1 },
  { q: "एक दिन में अधिकतम कितने घंटे काम?", o: ["8 घंटे", "10 घंटे", "12 घंटे", "कोई सीमा नहीं"], c: 2 },
  { q: "ओवरटाइम का भुगतान कितना होना चाहिए?", o: ["सामान्य", "1.5 गुना", "दोगुना", "तिगुना"], c: 2 },
  { q: "PF में कर्मचारी का योगदान?", o: ["8%", "10%", "12%", "15%"], c: 2 },
  { q: "मजदूरी न मिलने पर शिकायत कहाँ?", o: ["पुलिस", "श्रम आयुक्त", "कोर्ट", "ये सभी"], c: 3 },
  { q: "गर्भवती महिला को कितने दिन छुट्टी?", o: ["30", "60", "182", "365"], c: 2 },
];

/* ── Inject styles ── */
const injectStyles = () => {
  if (document.getElementById("mjr-styles")) return;
  const link = document.createElement("link");
  link.href = "https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@300;400;500;600;700;800;900&family=Cormorant+Garamond:wght@600;700&display=swap";
  link.rel = "stylesheet";
  document.head.appendChild(link);

  const s = document.createElement("style");
  s.id = "mjr-styles";
  s.textContent = `
    @keyframes mjr-fadeUp { from { opacity:0; transform:translateY(24px); } to { opacity:1; transform:translateY(0); } }
    @keyframes mjr-slideIn { from { opacity:0; transform:translateX(-16px); } to { opacity:1; transform:translateX(0); } }
    @keyframes mjr-pulse { 0%,100% { transform:scale(1); } 50% { transform:scale(1.05); } }
    @keyframes mjr-spin { to { transform:rotate(360deg); } }
    @keyframes mjr-glow { 0%,100% { box-shadow:0 0 20px rgba(255,153,51,0.2); } 50% { box-shadow:0 0 40px rgba(255,153,51,0.4); } }
    @keyframes mjr-float { 0%,100% { transform:translateY(0px); } 50% { transform:translateY(-8px); } }
    @keyframes mjr-typing { 0% { opacity:.3; } 50% { opacity:1; } 100% { opacity:.3; } }
    @keyframes mjr-gradient { 0% { background-position:0% 50%; } 50% { background-position:100% 50%; } 100% { background-position:0% 50%; } }
    @media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation-duration:0.01ms!important; transition-duration:0.01ms!important; } }
    .mjr-nav::-webkit-scrollbar { display:none; }
    .mjr-card-hover { transition:all 0.35s cubic-bezier(0.4,0,0.2,1); }
    .mjr-card-hover:hover { transform:translateY(-4px); box-shadow:0 20px 40px rgba(15,23,42,0.12); }
    .mjr-btn-glow:hover { box-shadow:0 8px 25px rgba(194,65,12,0.35); transform:translateY(-2px); }
    .mjr-input:focus { border-color:#c2410c!important; box-shadow:0 0 0 4px rgba(194,65,12,0.08)!important; outline:none; }
    .mjr-chat-scroll::-webkit-scrollbar { width:4px; }
    .mjr-chat-scroll::-webkit-scrollbar-thumb { background:#d4c8b8; border-radius:4px; }
  `;
  document.head.appendChild(s);
};

/* ══════════════════════════════════════════════════════════════
   DECORATIVE SVGs
   ══════════════════════════════════════════════════════════════ */
const AshokaSVG = ({ size = 40, color = "rgba(255,153,51,0.12)" }) => (
  <svg width={size} height={size} viewBox="0 0 100 100" style={{ flexShrink: 0 }}>
    <circle cx="50" cy="50" r="45" fill="none" stroke={color} strokeWidth="3" />
    <circle cx="50" cy="50" r="8" fill={color} />
    {Array.from({ length: 24 }).map((_, i) => (
      <line key={i} x1="50" y1="12" x2="50" y2="25" stroke={color} strokeWidth="2"
        transform={`rotate(${i * 15} 50 50)`} />
    ))}
  </svg>
);

const WaveDivider = () => (
  <svg viewBox="0 0 1200 60" preserveAspectRatio="none" style={{ width:"100%", height:32, display:"block" }}>
    <path d="M0,30 C200,55 400,5 600,30 C800,55 1000,5 1200,30 L1200,60 L0,60Z" fill="rgba(255,153,51,0.06)" />
    <path d="M0,40 C200,60 400,20 600,40 C800,60 1000,20 1200,40 L1200,60 L0,60Z" fill="rgba(19,136,8,0.04)" />
  </svg>
);

/* ══════════════════════════════════════════════════════════════
   MAIN APP COMPONENT
   ══════════════════════════════════════════════════════════════ */
export default function MajdoorApp() {
  const [tab, setTab] = useState("home");
  const [form, setForm] = useState({ name:"", phone:"", state:"", district:"", employer:"", issue:"", desc:"", date:"" });
  const [submitted, setSubmitted] = useState(false);
  const [genDoc, setGenDoc] = useState(null);
  const [rti, setRti] = useState({ name:"", dept:"", question:"" });
  const [rtiDoc, setRtiDoc] = useState(null);
  const [quiz, setQuiz] = useState({ i:0, score:0, ans:null, done:false });
  const [evidence, setEvidence] = useState([]);
  const [msgs, setMsgs] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [cases, setCases] = useState([]);
  const chatEnd = useRef(null);

  useEffect(() => { injectStyles(); }, []);
  useEffect(() => { chatEnd.current?.scrollIntoView({ behavior:"smooth" }); }, [msgs]);

  const callAI = async (prompt) => {
    try {
      const r = await fetch("https://api.anthropic.com/v1/messages", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ model:"claude-sonnet-4-20250514", max_tokens:1000,
          messages:[{ role:"user", content:prompt }] }),
      });
      const d = await r.json();
      return d.content?.map(c=>c.text||"").join("") || "माफ़ करें, जवाब नहीं मिला।";
    } catch { return "नेटवर्क समस्या। कृपया दोबारा कोशिश करें।"; }
  };

  const sendChat = async () => {
    if (!input.trim()) return;
    const q = input.trim(); setInput(""); setLoading(true);
    setMsgs(p=>[...p,{role:"user",text:q}]);
    const reply = await callAI(`आप एक अनुभवी भारतीय कानूनी सहायक हैं। मजदूरों की मदद हिंदी में करें। कानून का नाम, शिकायत का तरीका, हेल्पलाइन बताएं। सरल भाषा।\n\nसवाल: ${q}`);
    setMsgs(p=>[...p,{role:"bot",text:reply}]); setLoading(false);
  };

  const generateComplaint = async () => {
    if(!form.name||!form.issue||!form.desc||!form.state) return;
    const issue = ISSUE_TYPES.find(i=>i.id===form.issue); setLoading(true);
    const doc = await callAI(`कानूनी दस्तावेज़ लेखक बनें। औपचारिक शिकायत पत्र हिंदी में लिखें:\nनाम:${form.name}\nफ़ोन:${form.phone}\nराज्य:${form.state}, जिला:${form.district}\nमालिक:${form.employer}\nसमस्या:${issue?.label} (${issue?.law})\nविवरण:${form.desc}\nतारीख:${form.date||"आज"}\nविषय, सम्बोधन, विवरण, प्रार्थना, हस्ताक्षर शामिल करें।`);
    setGenDoc(doc); setLoading(false); setSubmitted(true);
    setCases(p=>[...p,{id:Date.now(),name:form.name,issue:issue?.label,state:form.state,date:new Date().toLocaleDateString("hi-IN"),status:"दर्ज"}]);
  };

  const generateRTI = async () => {
    if(!rti.question||!rti.dept) return; setLoading(true);
    const doc = await callAI(`RTI Act 2005 के तहत औपचारिक RTI आवेदन पत्र हिंदी में लिखें।\nआवेदक:${rti.name||"___"}\nविभाग:${rti.dept}\nजानकारी:${rti.question}`);
    setRtiDoc(doc); setLoading(false);
  };

  const TABS = [
    { id:"home", label:"होम", icon:"🏠" },
    { id:"chat", label:"AI सहायक", icon:"💬" },
    { id:"complaint", label:"शिकायत दर्ज", icon:"📝" },
    { id:"docs", label:"दस्तावेज़", icon:"📄" },
    { id:"evidence", label:"सबूत", icon:"📸" },
    { id:"tracker", label:"ट्रैकर", icon:"📊" },
    { id:"quiz", label:"क्विज़", icon:"🧠" },
    { id:"sos", label:"SOS", icon:"🆘" },
  ];

  return (
    <div style={{ fontFamily:"'Noto Sans Devanagari',sans-serif", color:"#1a1512", minHeight:"100vh",
      background:"linear-gradient(168deg, #faf6f0 0%, #f5ede0 30%, #f0e8d8 60%, #f5ede0 100%)", position:"relative", overflow:"hidden" }}>

      {/* ── BG TEXTURE ── */}
      <div style={{ position:"fixed",inset:0,zIndex:0,pointerEvents:"none",
        backgroundImage:`radial-gradient(ellipse at 15% 20%, rgba(255,153,51,0.08) 0%, transparent 50%),
          radial-gradient(ellipse at 85% 70%, rgba(19,136,8,0.05) 0%, transparent 50%),
          radial-gradient(ellipse at 50% 50%, rgba(30,41,82,0.03) 0%, transparent 60%)`,
      }} />
      <div style={{ position:"fixed",inset:0,zIndex:0,pointerEvents:"none",opacity:0.3,
        backgroundImage:`url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c4956a' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
      }} />

      {/* ══════ HEADER ══════ */}
      <header style={{
        background:"linear-gradient(135deg, #1e2952 0%, #0f1a3a 40%, #0a1128 100%)",
        position:"relative",zIndex:2,overflow:"hidden",
      }}>
        {/* Tricolor accent bar */}
        <div style={{ height:4,display:"flex" }}>
          <div style={{ flex:1,background:"#FF9933" }} />
          <div style={{ flex:1,background:"#ffffff" }} />
          <div style={{ flex:1,background:"#138808" }} />
        </div>
        {/* Floating decorative elements */}
        <div style={{ position:"absolute",right:20,top:12,opacity:0.06 }}>
          <AshokaSVG size={120} color="#fff" />
        </div>
        <div style={{ position:"absolute",left:-20,bottom:-20,opacity:0.04 }}>
          <AshokaSVG size={100} color="#FF9933" />
        </div>

        <div style={{ maxWidth:880,margin:"0 auto",padding:"22px 24px",display:"flex",alignItems:"center",gap:18,position:"relative",zIndex:1 }}>
          <div style={{
            width:56,height:56,borderRadius:14,
            background:"linear-gradient(135deg, #FF9933 0%, #e6821a 100%)",
            display:"flex",alignItems:"center",justifyContent:"center",
            fontSize:28,boxShadow:"0 4px 20px rgba(255,153,51,0.3)",
            animation:"mjr-glow 3s ease-in-out infinite",
          }}>⚖️</div>
          <div>
            <h1 style={{ margin:0,fontSize:24,color:"#fff",fontWeight:900,letterSpacing:"-0.5px",lineHeight:1.2 }}>
              मजदूर अधिकार सहायक
            </h1>
            <p style={{ margin:"3px 0 0",fontSize:13,color:"rgba(255,255,255,0.5)",fontWeight:400,letterSpacing:"1px" }}>
              WORKERS' RIGHTS PROTECTION PLATFORM
            </p>
          </div>
        </div>
      </header>

      {/* ══════ NAV ══════ */}
      <nav style={{
        position:"sticky",top:0,zIndex:20,
        background:"rgba(250,246,240,0.85)",backdropFilter:"blur(16px)",WebkitBackdropFilter:"blur(16px)",
        borderBottom:"1px solid rgba(194,149,106,0.15)",
        boxShadow:"0 4px 20px rgba(0,0,0,0.04)",
      }}>
        <div className="mjr-nav" style={{ display:"flex",overflowX:"auto",maxWidth:880,margin:"0 auto",scrollbarWidth:"none",gap:2,padding:"0 8px" }}>
          {TABS.map(t => (
            <button key={t.id} onClick={()=>setTab(t.id)} style={{
              display:"flex",flexDirection:"column",alignItems:"center",gap:1,
              padding:"12px 16px",border:"none",background:"transparent",
              cursor:"pointer",fontFamily:"inherit",flexShrink:0,
              borderBottom: tab===t.id ? "3px solid #c2410c" : "3px solid transparent",
              color: tab===t.id ? "#c2410c" : "#8c7b6b",
              transition:"all 0.3s cubic-bezier(0.4,0,0.2,1)",
              transform: tab===t.id ? "scale(1)" : "scale(0.95)",
            }}>
              <span style={{ fontSize:20,lineHeight:1,filter: tab===t.id ? "none" : "grayscale(0.5)" }}>{t.icon}</span>
              <span style={{ fontSize:10,fontWeight: tab===t.id ? 800 : 500,letterSpacing:"0.5px" }}>{t.label}</span>
            </button>
          ))}
        </div>
      </nav>

      {/* ══════ MAIN CONTENT ══════ */}
      <main style={{ maxWidth:880,margin:"0 auto",padding:"24px 16px 60px",position:"relative",zIndex:1 }}>

        {/* ════════════════ HOME ════════════════ */}
        {tab==="home" && (
          <div style={{ animation:"mjr-fadeUp 0.5s ease" }}>
            {/* Hero */}
            <div style={{
              position:"relative",borderRadius:20,overflow:"hidden",marginBottom:28,
              background:"linear-gradient(135deg, #1e2952 0%, #0f1a3a 50%, #1a1040 100%)",
              boxShadow:"0 20px 60px rgba(15,26,58,0.25)",
            }}>
              {/* Decorative circles */}
              <div style={{ position:"absolute",right:-30,top:-30,width:180,height:180,borderRadius:"50%",
                background:"radial-gradient(circle, rgba(255,153,51,0.15) 0%, transparent 70%)" }} />
              <div style={{ position:"absolute",left:-20,bottom:-40,width:140,height:140,borderRadius:"50%",
                background:"radial-gradient(circle, rgba(19,136,8,0.1) 0%, transparent 70%)" }} />

              <div style={{ position:"relative",zIndex:1,padding:"36px 28px" }}>
                <div style={{ display:"flex",gap:8,marginBottom:16 }}>
                  {["🇮🇳","⚖️","✊"].map((e,i)=>(
                    <span key={i} style={{ fontSize:28,animation:`mjr-float 3s ease-in-out ${i*0.4}s infinite` }}>{e}</span>
                  ))}
                </div>
                <h2 style={{ margin:"0 0 12px",fontSize:28,color:"#fff",fontWeight:900,lineHeight:1.3,
                  background:"linear-gradient(90deg, #fff 0%, #FFD699 100%)",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent" }}>
                  आपके अधिकार,<br/>आपकी ताकत
                </h2>
                <p style={{ margin:"0 0 24px",fontSize:15,color:"rgba(255,255,255,0.6)",lineHeight:1.9,maxWidth:480 }}>
                  भारत के हर मजदूर के लिए — अपने अधिकार जानें, शिकायत दर्ज करें, कानूनी दस्तावेज़ बनाएं, सबूत जमा करें।
                </p>
                <div style={{ display:"flex",gap:12,flexWrap:"wrap" }}>
                  <button className="mjr-btn-glow" onClick={()=>setTab("complaint")} style={{
                    padding:"13px 28px",background:"linear-gradient(135deg,#c2410c,#ea580c)",color:"#fff",
                    border:"none",borderRadius:12,fontSize:15,fontWeight:700,cursor:"pointer",fontFamily:"inherit",
                    boxShadow:"0 4px 20px rgba(194,65,12,0.3)",transition:"all 0.3s",
                  }}>📝 शिकायत दर्ज करें</button>
                  <button className="mjr-btn-glow" onClick={()=>setTab("chat")} style={{
                    padding:"13px 28px",background:"rgba(255,255,255,0.1)",color:"#fff",
                    border:"1px solid rgba(255,255,255,0.2)",borderRadius:12,fontSize:15,fontWeight:600,
                    cursor:"pointer",fontFamily:"inherit",backdropFilter:"blur(8px)",transition:"all 0.3s",
                  }}>💬 AI से पूछें</button>
                </div>
              </div>
            </div>

            <WaveDivider />

            {/* Feature Cards */}
            <h3 style={{ margin:"12px 0 18px",fontSize:18,fontWeight:800,color:"#1e2952",display:"flex",alignItems:"center",gap:10 }}>
              <AshokaSVG size={28} color="#c2410c" /> सेवाएं
            </h3>
            <div style={{ display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(155px,1fr))",gap:14 }}>
              {[
                {icon:"📝",title:"ऑटो शिकायत",desc:"शिकायत पत्र AI से बनाएं",tab:"complaint",accent:"#c2410c"},
                {icon:"💬",title:"AI सहायक",desc:"कानूनी सवाल पूछें",tab:"chat",accent:"#1e2952"},
                {icon:"📄",title:"RTI पत्र",desc:"RTI आवेदन तैयार करें",tab:"docs",accent:"#0d6938"},
                {icon:"📸",title:"सबूत जमा",desc:"फ़ोटो और दस्तावेज़ सेव",tab:"evidence",accent:"#7c3aed"},
                {icon:"📊",title:"केस ट्रैकर",desc:"शिकायत की स्थिति देखें",tab:"tracker",accent:"#0369a1"},
                {icon:"🧠",title:"अधिकार क्विज़",desc:"खेल-खेल में सीखें",tab:"quiz",accent:"#b45309"},
              ].map((f,i)=>(
                <button key={i} className="mjr-card-hover" onClick={()=>setTab(f.tab)} style={{
                  background:"rgba(255,255,255,0.7)",backdropFilter:"blur(8px)",
                  borderRadius:16,padding:"22px 16px",
                  border:"1px solid rgba(194,149,106,0.12)",
                  cursor:"pointer",fontFamily:"inherit",textAlign:"center",
                  display:"flex",flexDirection:"column",alignItems:"center",gap:8,
                  animation:`mjr-fadeUp 0.4s ease ${i*0.07}s both`,
                }}>
                  <span style={{
                    fontSize:30,width:52,height:52,borderRadius:14,
                    background:`linear-gradient(135deg, ${f.accent}10, ${f.accent}20)`,
                    display:"flex",alignItems:"center",justifyContent:"center",
                  }}>{f.icon}</span>
                  <strong style={{ fontSize:14,color:"#1e2952",fontWeight:800 }}>{f.title}</strong>
                  <span style={{ fontSize:12,color:"#8c7b6b",lineHeight:1.5 }}>{f.desc}</span>
                </button>
              ))}
            </div>

            {/* Emergency Banner */}
            <button onClick={()=>setTab("sos")} style={{
              width:"100%",marginTop:24,padding:"18px 20px",
              background:"linear-gradient(135deg,#dc2626,#991b1b)",
              borderRadius:16,border:"none",cursor:"pointer",fontFamily:"inherit",
              display:"flex",alignItems:"center",justifyContent:"center",gap:12,
              animation:"mjr-pulse 2s ease-in-out infinite",
              boxShadow:"0 8px 30px rgba(220,38,38,0.2)",
            }}>
              <span style={{ fontSize:28 }}>🆘</span>
              <span style={{ color:"#fff",fontSize:16,fontWeight:800 }}>आपातकालीन मदद — हेल्पलाइन नंबर</span>
            </button>
          </div>
        )}

        {/* ════════════════ CHAT ════════════════ */}
        {tab==="chat" && (
          <div style={{ animation:"mjr-fadeUp 0.4s ease" }}>
            <SectionHead icon="💬" title="AI कानूनी सहायक" desc="अपनी समस्या बताएं — AI कानूनी सलाह देगा" />

            <div style={{ display:"flex",gap:8,flexWrap:"wrap",marginBottom:16 }}>
              {["न्यूनतम वेतन कितना है?","मालिक पैसे नहीं दे रहा","ओवरटाइम के नियम","बिना नोटिस निकाला"].map(q=>(
                <button key={q} className="mjr-card-hover" onClick={()=>setInput(q)} style={{
                  padding:"8px 16px",borderRadius:24,
                  border:"1px solid rgba(194,149,106,0.2)",
                  background:"rgba(255,255,255,0.6)",backdropFilter:"blur(8px)",
                  fontSize:13,cursor:"pointer",fontFamily:"inherit",color:"#1e2952",fontWeight:500,
                }}>✦ {q}</button>
              ))}
            </div>

            <div className="mjr-chat-scroll" style={{
              background:"linear-gradient(180deg, rgba(245,237,224,0.5) 0%, rgba(240,232,216,0.3) 100%)",
              borderRadius:20,padding:18,minHeight:320,maxHeight:440,overflowY:"auto",
              border:"1px solid rgba(194,149,106,0.12)",
              boxShadow:"inset 0 2px 12px rgba(0,0,0,0.03)",
              display:"flex",flexDirection:"column",gap:14,
            }}>
              {msgs.length===0 && (
                <div style={{ display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",height:280,gap:12,color:"#b8a894" }}>
                  <span style={{ fontSize:52,animation:"mjr-float 3s ease-in-out infinite" }}>⚖️</span>
                  <p style={{ fontSize:15,fontWeight:500 }}>अपना सवाल पूछें...</p>
                  <p style={{ fontSize:12,opacity:0.6 }}>हिंदी या English में लिख सकते हैं</p>
                </div>
              )}
              {msgs.map((m,i)=>(
                <div key={i} style={{ display:"flex",justifyContent:m.role==="user"?"flex-end":"flex-start",animation:"mjr-slideIn 0.3s ease" }}>
                  <div style={{
                    maxWidth:"82%",padding:"12px 18px",fontSize:14,lineHeight:1.8,whiteSpace:"pre-wrap",
                    borderRadius: m.role==="user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                    ...(m.role==="user"
                      ? { background:"linear-gradient(135deg,#1e2952,#0f1a3a)",color:"#fff",boxShadow:"0 4px 15px rgba(30,41,82,0.15)" }
                      : { background:"rgba(255,255,255,0.85)",color:"#1a1512",border:"1px solid rgba(194,149,106,0.12)",backdropFilter:"blur(8px)",boxShadow:"0 2px 10px rgba(0,0,0,0.04)" }),
                  }}>{m.text}</div>
                </div>
              ))}
              {loading && (
                <div style={{ display:"flex",gap:6,padding:"12px 18px" }}>
                  {[0,1,2].map(i=>(
                    <div key={i} style={{ width:8,height:8,borderRadius:"50%",background:"#c2410c",animation:`mjr-typing 1s ease ${i*0.2}s infinite` }} />
                  ))}
                </div>
              )}
              <div ref={chatEnd} />
            </div>

            <div style={{ display:"flex",gap:10,marginTop:14 }}>
              <input className="mjr-input" value={input} onChange={e=>setInput(e.target.value)}
                onKeyDown={e=>e.key==="Enter"&&sendChat()}
                placeholder="अपनी समस्या यहाँ लिखें..."
                style={{
                  flex:1,padding:"14px 20px",borderRadius:14,fontSize:14,fontFamily:"inherit",
                  border:"1.5px solid rgba(194,149,106,0.2)",background:"rgba(255,255,255,0.7)",
                  backdropFilter:"blur(8px)",outline:"none",transition:"all 0.3s",
                }} />
              <button className="mjr-btn-glow" onClick={sendChat} style={{
                padding:"14px 24px",background:"linear-gradient(135deg,#c2410c,#ea580c)",
                color:"#fff",border:"none",borderRadius:14,fontSize:14,fontWeight:700,
                cursor:"pointer",fontFamily:"inherit",boxShadow:"0 4px 15px rgba(194,65,12,0.25)",transition:"all 0.3s",
              }}>भेजें ➤</button>
            </div>
          </div>
        )}

        {/* ════════════════ COMPLAINT ════════════════ */}
        {tab==="complaint" && (
          <div style={{ animation:"mjr-fadeUp 0.4s ease" }}>
            <SectionHead icon="📝" title="शिकायत दर्ज करें" desc="जानकारी भरें — शिकायत पत्र और नजदीकी कार्यालय स्वचालित मिलेगा" />

            {!submitted ? (
              <GlassCard>
                {/* Step indicator */}
                <div style={{ display:"flex",gap:6,marginBottom:24 }}>
                  {["जानकारी","समस्या","विवरण"].map((s,i)=>(
                    <div key={i} style={{ flex:1,textAlign:"center" }}>
                      <div style={{ height:4,borderRadius:4,background: i===0?"#c2410c":i===1?(form.issue?"#c2410c":"#e5ddd2"):form.desc?"#c2410c":"#e5ddd2",transition:"all 0.4s" }} />
                      <span style={{ fontSize:11,color:"#8c7b6b",fontWeight:500 }}>{s}</span>
                    </div>
                  ))}
                </div>

                <div style={{ display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(230px,1fr))",gap:18 }}>
                  <FormField label="आपका नाम" required>
                    <Input value={form.name} onChange={v=>setForm(p=>({...p,name:v}))} placeholder="पूरा नाम" />
                  </FormField>
                  <FormField label="फ़ोन नंबर">
                    <Input value={form.phone} onChange={v=>setForm(p=>({...p,phone:v}))} placeholder="मोबाइल नंबर" />
                  </FormField>
                  <FormField label="राज्य" required>
                    <select className="mjr-input" value={form.state} onChange={e=>setForm(p=>({...p,state:e.target.value}))} style={inputStyle}>
                      <option value="">-- राज्य चुनें --</option>
                      {Object.keys(STATES).map(s=><option key={s} value={s}>{s}</option>)}
                    </select>
                  </FormField>
                  <FormField label="जिला">
                    <Input value={form.district} onChange={v=>setForm(p=>({...p,district:v}))} placeholder="जिले का नाम" />
                  </FormField>
                  <FormField label="मालिक / कंपनी का नाम">
                    <Input value={form.employer} onChange={v=>setForm(p=>({...p,employer:v}))} placeholder="कंपनी / ठेकेदार" />
                  </FormField>
                  <FormField label="घटना की तारीख">
                    <input className="mjr-input" type="date" value={form.date} onChange={e=>setForm(p=>({...p,date:e.target.value}))} style={inputStyle} />
                  </FormField>
                </div>

                <div style={{ marginTop:24 }}>
                  <span style={{ fontSize:13,fontWeight:700,color:"#1e2952" }}>समस्या का प्रकार <span style={{ color:"#c2410c" }}>*</span></span>
                  <div style={{ display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(95px,1fr))",gap:10,marginTop:12 }}>
                    {ISSUE_TYPES.map(it=>(
                      <button key={it.id} onClick={()=>setForm(p=>({...p,issue:it.id}))}
                        className="mjr-card-hover" style={{
                          display:"flex",flexDirection:"column",alignItems:"center",gap:6,
                          padding:"14px 8px",borderRadius:14,fontFamily:"inherit",cursor:"pointer",textAlign:"center",
                          border: form.issue===it.id ? "2px solid #c2410c" : "1.5px solid rgba(194,149,106,0.15)",
                          background: form.issue===it.id ? "linear-gradient(135deg,#fff7ed,#fef3c7)" : "rgba(255,255,255,0.5)",
                          boxShadow: form.issue===it.id ? "0 4px 20px rgba(194,65,12,0.12)" : "none",
                          transition:"all 0.3s",
                        }}>
                        <span style={{ fontSize:24 }}>{it.icon}</span>
                        <span style={{ fontSize:11,fontWeight:600,lineHeight:1.4,color:"#1e2952" }}>{it.label}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {form.issue && (
                  <div style={{
                    marginTop:18,padding:"14px 18px",borderRadius:14,
                    background:"linear-gradient(135deg,#eff6ff,#dbeafe)",
                    border:"1px solid #93c5fd",animation:"mjr-fadeUp 0.3s ease",
                  }}>
                    <span style={{ fontSize:13,color:"#1e40af",fontWeight:500 }}>
                      📜 लागू कानून: <strong>{ISSUE_TYPES.find(i=>i.id===form.issue)?.law}</strong>
                    </span>
                  </div>
                )}

                <FormField label="समस्या का विवरण" required style={{ marginTop:20 }}>
                  <textarea className="mjr-input" value={form.desc} onChange={e=>setForm(p=>({...p,desc:e.target.value}))}
                    placeholder="क्या हुआ, कब हुआ, कैसे हुआ — विस्तार से बताएं..."
                    style={{ ...inputStyle, minHeight:120,resize:"vertical" }} />
                </FormField>

                {form.state && STATES[form.state] && (
                  <div style={{
                    marginTop:18,padding:"16px 18px",borderRadius:14,
                    background:"linear-gradient(135deg,#fffbeb,#fef3c7)",
                    border:"1px solid #fde68a",animation:"mjr-fadeUp 0.3s ease",
                  }}>
                    <div style={{ display:"flex",alignItems:"center",gap:8,marginBottom:6 }}>
                      <span style={{ fontSize:18 }}>📍</span>
                      <strong style={{ color:"#92400e",fontSize:14 }}>नजदीकी श्रम कार्यालय</strong>
                    </div>
                    <p style={{ margin:0,fontSize:13,color:"#78350f",lineHeight:1.7 }}>
                      {STATES[form.state].office}<br/>📞 {STATES[form.state].phone}
                    </p>
                  </div>
                )}

                <button className="mjr-btn-glow" onClick={generateComplaint} disabled={loading} style={{
                  width:"100%",marginTop:24,padding:"16px 0",
                  background: loading ? "#9ca3af" : "linear-gradient(135deg,#c2410c,#ea580c)",
                  color:"#fff",border:"none",borderRadius:14,fontSize:16,fontWeight:800,
                  cursor: loading ? "wait" : "pointer",fontFamily:"inherit",
                  boxShadow: loading ? "none" : "0 8px 30px rgba(194,65,12,0.25)",transition:"all 0.3s",
                }}>
                  {loading ? "⏳ बनाया जा रहा है..." : "📄 शिकायत पत्र बनाएं और दर्ज करें"}
                </button>
              </GlassCard>
            ) : (
              <GlassCard>
                <div style={{ textAlign:"center",marginBottom:24 }}>
                  <div style={{ fontSize:56,animation:"mjr-pulse 1.5s ease" }}>✅</div>
                  <h3 style={{ color:"#15803d",margin:"10px 0 4px",fontSize:20 }}>शिकायत सफलतापूर्वक दर्ज!</h3>
                  <p style={{ color:"#8c7b6b",fontSize:14 }}>पत्र डाउनलोड या प्रिंट करें और श्रम कार्यालय में जमा करें।</p>
                </div>
                <div style={{
                  background:"rgba(250,246,240,0.8)",border:"1px solid rgba(194,149,106,0.15)",
                  borderRadius:14,padding:22,fontSize:13,lineHeight:2.1,whiteSpace:"pre-wrap",
                  maxHeight:400,overflowY:"auto",fontFamily:"inherit",
                }}>{genDoc}</div>
                <div style={{ display:"flex",gap:12,marginTop:18,flexWrap:"wrap" }}>
                  <SecBtn onClick={()=>{ const b=new Blob([genDoc],{type:"text/plain;charset=utf-8"}); const u=URL.createObjectURL(b); const a=document.createElement("a"); a.href=u; a.download="shikayat.txt"; a.click(); }}>⬇️ डाउनलोड</SecBtn>
                  <SecBtn onClick={()=>navigator.clipboard?.writeText(genDoc)}>📋 कॉपी</SecBtn>
                  <button className="mjr-btn-glow" onClick={()=>{setSubmitted(false);setForm({name:"",phone:"",state:"",district:"",employer:"",issue:"",desc:"",date:""});setGenDoc(null);}} style={{
                    padding:"11px 24px",background:"linear-gradient(135deg,#c2410c,#ea580c)",color:"#fff",
                    border:"none",borderRadius:12,fontSize:14,fontWeight:700,cursor:"pointer",fontFamily:"inherit",transition:"all 0.3s",
                  }}>➕ नई शिकायत</button>
                </div>
              </GlassCard>
            )}
          </div>
        )}

        {/* ════════════════ DOCUMENTS ════════════════ */}
        {tab==="docs" && (
          <div style={{ animation:"mjr-fadeUp 0.4s ease" }}>
            <SectionHead icon="📄" title="कानूनी दस्तावेज़ बनाएं" desc="RTI आवेदन या कानूनी नोटिस AI से तैयार करें" />
            <GlassCard>
              <h3 style={{ margin:"0 0 20px",fontSize:17,fontWeight:800,color:"#1e2952",display:"flex",alignItems:"center",gap:8 }}>
                <span style={{ fontSize:22 }}>📜</span> RTI आवेदन पत्र
              </h3>
              <FormField label="आपका नाम"><Input value={rti.name} onChange={v=>setRti(p=>({...p,name:v}))} placeholder="पूरा नाम" /></FormField>
              <FormField label="विभाग / कार्यालय" required><Input value={rti.dept} onChange={v=>setRti(p=>({...p,dept:v}))} placeholder="जैसे: श्रम विभाग" /></FormField>
              <FormField label="क्या जानकारी चाहिए?" required>
                <textarea className="mjr-input" value={rti.question} onChange={e=>setRti(p=>({...p,question:e.target.value}))}
                  placeholder="विस्तार से लिखें..." style={{...inputStyle,minHeight:100}} />
              </FormField>
              <button className="mjr-btn-glow" onClick={generateRTI} disabled={loading} style={{
                width:"100%",marginTop:16,padding:"14px 0",
                background:loading?"#9ca3af":"linear-gradient(135deg,#0d6938,#15803d)",color:"#fff",
                border:"none",borderRadius:14,fontSize:15,fontWeight:700,cursor:loading?"wait":"pointer",
                fontFamily:"inherit",boxShadow:"0 6px 20px rgba(13,105,56,0.2)",transition:"all 0.3s",
              }}>{loading ? "⏳ बनाया जा रहा है..." : "📄 RTI पत्र बनाएं"}</button>
              {rtiDoc && (
                <>
                  <div style={{ background:"rgba(250,246,240,0.8)",border:"1px solid rgba(194,149,106,0.15)",borderRadius:14,padding:22,fontSize:13,lineHeight:2.1,whiteSpace:"pre-wrap",maxHeight:400,overflowY:"auto",fontFamily:"inherit",marginTop:20 }}>{rtiDoc}</div>
                  <div style={{ display:"flex",gap:12,marginTop:14 }}>
                    <SecBtn onClick={()=>{ const b=new Blob([rtiDoc],{type:"text/plain;charset=utf-8"}); const u=URL.createObjectURL(b); const a=document.createElement("a"); a.href=u; a.download="rti.txt"; a.click(); }}>⬇️ डाउनलोड</SecBtn>
                    <SecBtn onClick={()=>navigator.clipboard?.writeText(rtiDoc)}>📋 कॉपी</SecBtn>
                  </div>
                </>
              )}
            </GlassCard>
          </div>
        )}

        {/* ════════════════ EVIDENCE ════════════════ */}
        {tab==="evidence" && (
          <div style={{ animation:"mjr-fadeUp 0.4s ease" }}>
            <SectionHead icon="📸" title="सबूत जमा करें" desc="फ़ोटो और दस्तावेज़ अपलोड करें — तारीख स्वचालित दर्ज होगी" />
            <GlassCard>
              <label style={{
                display:"flex",flexDirection:"column",alignItems:"center",gap:10,padding:"36px 20px",
                border:"2px dashed rgba(194,149,106,0.3)",borderRadius:18,cursor:"pointer",
                background:"rgba(255,255,255,0.3)",transition:"all 0.3s",
              }}>
                <input type="file" accept="image/*,application/pdf" multiple style={{ display:"none" }}
                  onChange={e=>{
                    Array.from(e.target.files||[]).forEach(f=>{
                      const r=new FileReader();
                      r.onload=()=>setEvidence(p=>[...p,{name:f.name,type:f.type,size:f.size,url:r.result,time:new Date().toLocaleString("hi-IN")}]);
                      r.readAsDataURL(f);
                    });
                  }} />
                <span style={{ fontSize:44 }}>📁</span>
                <strong style={{ fontSize:15,color:"#1e2952" }}>फ़ोटो या PDF अपलोड करें</strong>
                <span style={{ fontSize:12,color:"#8c7b6b" }}>क्लिक करें या फ़ाइल खींचकर छोड़ें</span>
              </label>

              {evidence.length>0 && (
                <div style={{ marginTop:24 }}>
                  <h4 style={{ margin:"0 0 14px",color:"#1e2952",fontWeight:700 }}>जमा सबूत ({evidence.length})</h4>
                  {evidence.map((f,i)=>(
                    <div key={i} style={{
                      display:"flex",gap:14,alignItems:"center",padding:14,marginTop:8,
                      borderRadius:14,background:"rgba(255,255,255,0.5)",border:"1px solid rgba(194,149,106,0.1)",
                      animation:"mjr-slideIn 0.3s ease",
                    }}>
                      {f.type.startsWith("image") ?
                        <img src={f.url} alt="" style={{ width:56,height:56,objectFit:"cover",borderRadius:12 }} /> :
                        <div style={{ width:56,height:56,borderRadius:12,background:"#fee2e2",display:"flex",alignItems:"center",justifyContent:"center",fontSize:24 }}>📄</div>
                      }
                      <div style={{ flex:1,minWidth:0 }}>
                        <div style={{ fontSize:13,fontWeight:700,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap" }}>{f.name}</div>
                        <div style={{ fontSize:12,color:"#8c7b6b" }}>🕐 {f.time} • {(f.size/1024).toFixed(1)} KB</div>
                      </div>
                      <button onClick={()=>setEvidence(p=>p.filter((_,j)=>j!==i))} style={{
                        width:34,height:34,borderRadius:10,border:"none",background:"#fee2e2",color:"#dc2626",
                        cursor:"pointer",fontSize:14,display:"flex",alignItems:"center",justifyContent:"center",fontFamily:"inherit",
                      }}>✕</button>
                    </div>
                  ))}
                </div>
              )}
            </GlassCard>
          </div>
        )}

        {/* ════════════════ TRACKER ════════════════ */}
        {tab==="tracker" && (
          <div style={{ animation:"mjr-fadeUp 0.4s ease" }}>
            <SectionHead icon="📊" title="केस ट्रैकर" desc="दर्ज शिकायतों की स्थिति" />
            {cases.length===0 ? (
              <div style={{ textAlign:"center",padding:"56px 20px",color:"#8c7b6b" }}>
                <span style={{ fontSize:56,display:"block",marginBottom:12,animation:"mjr-float 3s ease-in-out infinite" }}>📋</span>
                <p style={{ fontSize:16,fontWeight:600 }}>अभी कोई शिकायत नहीं</p>
                <button className="mjr-btn-glow" onClick={()=>setTab("complaint")} style={{
                  marginTop:16,padding:"12px 28px",background:"linear-gradient(135deg,#c2410c,#ea580c)",
                  color:"#fff",border:"none",borderRadius:12,fontSize:14,fontWeight:700,cursor:"pointer",fontFamily:"inherit",transition:"all 0.3s",
                }}>📝 शिकायत दर्ज करें</button>
              </div>
            ) : cases.map(c=>(
              <GlassCard key={c.id} style={{ marginBottom:14 }}>
                <div style={{ display:"flex",justifyContent:"space-between",alignItems:"center",flexWrap:"wrap",gap:8 }}>
                  <strong style={{ fontSize:16,color:"#1e2952" }}>{c.name}</strong>
                  <span style={{
                    padding:"5px 14px",borderRadius:24,fontSize:12,fontWeight:700,
                    background:"linear-gradient(135deg,#dbeafe,#eff6ff)",color:"#1e40af",
                    border:"1px solid #93c5fd",
                  }}>{c.status}</span>
                </div>
                <p style={{ margin:"10px 0 0",fontSize:13,color:"#8c7b6b" }}>
                  समस्या: {c.issue} | राज्य: {c.state} | तारीख: {c.date}
                </p>
                <div style={{ height:8,borderRadius:8,marginTop:14,background:"rgba(194,149,106,0.1)",overflow:"hidden" }}>
                  <div style={{ height:"100%",width:"33%",borderRadius:8,
                    background:"linear-gradient(90deg,#FF9933,#138808)",transition:"width 0.6s" }} />
                </div>
                <div style={{ display:"flex",justifyContent:"space-between",marginTop:6,fontSize:11,color:"#b8a894" }}>
                  <span>● दर्ज</span><span>○ समीक्षा</span><span>○ समाधान</span>
                </div>
              </GlassCard>
            ))}
          </div>
        )}

        {/* ════════════════ QUIZ ════════════════ */}
        {tab==="quiz" && (
          <div style={{ animation:"mjr-fadeUp 0.4s ease" }}>
            <SectionHead icon="🧠" title="अपने अधिकार जानें" desc="क्विज़ खेलें और अपने कानूनी अधिकार सीखें" />
            <GlassCard>
              {!quiz.done ? (
                <>
                  <div style={{ display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:18 }}>
                    <span style={{ fontSize:13,color:"#8c7b6b",fontWeight:500 }}>सवाल {quiz.i+1} / {QUIZ.length}</span>
                    <span style={{
                      padding:"4px 14px",borderRadius:20,fontSize:13,fontWeight:800,
                      background:"linear-gradient(135deg,#1e2952,#0f1a3a)",color:"#FFD699",
                    }}>⭐ {quiz.score}</span>
                  </div>
                  <div style={{ height:6,borderRadius:6,background:"rgba(194,149,106,0.1)",overflow:"hidden",marginBottom:24 }}>
                    <div style={{ height:"100%",borderRadius:6,background:"linear-gradient(90deg,#FF9933,#c2410c)",
                      width:`${((quiz.i+1)/QUIZ.length)*100}%`,transition:"width 0.5s cubic-bezier(0.4,0,0.2,1)" }} />
                  </div>
                  <h3 style={{ margin:"0 0 20px",fontSize:18,fontWeight:700,lineHeight:1.7,color:"#1e2952" }}>
                    {QUIZ[quiz.i].q}
                  </h3>
                  <div style={{ display:"flex",flexDirection:"column",gap:10 }}>
                    {QUIZ[quiz.i].o.map((opt,j)=>{
                      const answered=quiz.ans!==null;
                      const correct=j===QUIZ[quiz.i].c;
                      const selected=j===quiz.ans;
                      return (
                        <button key={j} disabled={answered} onClick={()=>setQuiz(p=>({...p,ans:j,score:j===QUIZ[p.i].c?p.score+1:p.score}))}
                          style={{
                            padding:"15px 20px",borderRadius:14,fontSize:15,fontWeight:600,
                            fontFamily:"inherit",cursor:answered?"default":"pointer",textAlign:"left",
                            border: answered&&correct ? "2px solid #22c55e" : answered&&selected&&!correct ? "2px solid #ef4444" : "1.5px solid rgba(194,149,106,0.15)",
                            background: answered&&correct ? "linear-gradient(135deg,#dcfce7,#d1fae5)" : answered&&selected&&!correct ? "linear-gradient(135deg,#fee2e2,#fecaca)" : "rgba(255,255,255,0.5)",
                            color:"#1e2952",transition:"all 0.3s",
                            transform: answered&&(correct||selected) ? "scale(1.01)" : "scale(1)",
                          }}>
                          <span style={{ marginRight:10,display:"inline-flex",width:24,height:24,borderRadius:8,
                            background: answered&&correct ? "#22c55e" : answered&&selected ? "#ef4444" : "rgba(194,149,106,0.1)",
                            color: answered&&(correct||selected) ? "#fff" : "#8c7b6b",
                            alignItems:"center",justifyContent:"center",fontSize:12,fontWeight:800,
                          }}>{answered&&correct?"✓":answered&&selected?"✕":String.fromCharCode(65+j)}</span>
                          {opt}
                        </button>
                      );
                    })}
                  </div>
                  {quiz.ans!==null && (
                    <button className="mjr-btn-glow" onClick={()=>{
                      if(quiz.i+1>=QUIZ.length) setQuiz(p=>({...p,done:true}));
                      else setQuiz(p=>({...p,i:p.i+1,ans:null}));
                    }} style={{
                      width:"100%",marginTop:20,padding:"14px 0",
                      background:"linear-gradient(135deg,#1e2952,#0f1a3a)",color:"#fff",
                      border:"none",borderRadius:14,fontSize:15,fontWeight:700,cursor:"pointer",fontFamily:"inherit",transition:"all 0.3s",
                    }}>{quiz.i+1>=QUIZ.length ? "🏆 नतीजा देखें" : "अगला सवाल ➤"}</button>
                  )}
                </>
              ) : (
                <div style={{ textAlign:"center",padding:"20px 0" }}>
                  <div style={{ fontSize:64,animation:"mjr-pulse 2s ease infinite" }}>{quiz.score>=4?"🏆":quiz.score>=2?"👍":"📚"}</div>
                  <h3 style={{ margin:"16px 0 6px",fontSize:26,fontWeight:900,
                    background:"linear-gradient(90deg,#1e2952,#c2410c)",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent" }}>
                    {quiz.score} / {QUIZ.length}
                  </h3>
                  <p style={{ color:"#8c7b6b",fontSize:15,marginBottom:24 }}>
                    {quiz.score>=4 ? "बहुत बढ़िया! आप अपने अधिकार जानते हैं!" : "और सीखें! अधिकार जानना ज़रूरी है।"}
                  </p>
                  <button className="mjr-btn-glow" onClick={()=>setQuiz({i:0,score:0,ans:null,done:false})} style={{
                    padding:"14px 32px",background:"linear-gradient(135deg,#c2410c,#ea580c)",color:"#fff",
                    border:"none",borderRadius:14,fontSize:15,fontWeight:700,cursor:"pointer",fontFamily:"inherit",transition:"all 0.3s",
                  }}>🔄 फिर से खेलें</button>
                </div>
              )}
            </GlassCard>
          </div>
        )}

        {/* ════════════════ SOS ════════════════ */}
        {tab==="sos" && (
          <div style={{ animation:"mjr-fadeUp 0.4s ease" }}>
            <div style={{
              borderRadius:20,overflow:"hidden",marginBottom:24,
              background:"linear-gradient(135deg,#dc2626 0%,#991b1b 60%,#7f1d1d 100%)",
              padding:"28px 24px",textAlign:"center",position:"relative",
              boxShadow:"0 12px 40px rgba(220,38,38,0.2)",
              animation:"mjr-glow 2s ease-in-out infinite",
            }}>
              <div style={{ position:"absolute",inset:0,background:"radial-gradient(circle at 50% 0%, rgba(255,255,255,0.08) 0%, transparent 60%)" }} />
              <span style={{ fontSize:44,display:"block",marginBottom:8,position:"relative" }}>🆘</span>
              <h2 style={{ margin:0,fontSize:22,color:"#fff",fontWeight:900,position:"relative" }}>आपातकालीन सहायता</h2>
              <p style={{ margin:"6px 0 0",color:"#fecaca",fontSize:13,position:"relative" }}>तुरंत मदद के लिए नीचे कॉल करें</p>
            </div>

            <div style={{ display:"flex",flexDirection:"column",gap:12 }}>
              {HELPLINES.map((h,i)=>(
                <div key={i} className="mjr-card-hover" style={{
                  display:"flex",alignItems:"center",gap:14,padding:"16px 18px",
                  background:"rgba(255,255,255,0.7)",backdropFilter:"blur(8px)",
                  borderRadius:16,border:"1px solid rgba(194,149,106,0.12)",
                  animation:`mjr-slideIn 0.3s ease ${i*0.06}s both`,
                }}>
                  <span style={{
                    fontSize:24,width:48,height:48,borderRadius:14,
                    background:"linear-gradient(135deg,#dcfce7,#d1fae5)",
                    display:"flex",alignItems:"center",justifyContent:"center",
                  }}>{h.icon}</span>
                  <div style={{ flex:1 }}>
                    <div style={{ fontWeight:700,fontSize:15,color:"#1e2952" }}>{h.name}</div>
                    <div style={{ fontSize:12,color:"#8c7b6b" }}>{h.desc}</div>
                  </div>
                  <a href={`tel:${h.number}`} style={{
                    padding:"10px 18px",borderRadius:12,fontWeight:800,fontSize:14,
                    background:"linear-gradient(135deg,#dcfce7,#bbf7d0)",color:"#15803d",
                    textDecoration:"none",whiteSpace:"nowrap",border:"1px solid #86efac",
                    boxShadow:"0 2px 10px rgba(21,128,61,0.1)",
                  }}>📞 {h.number}</a>
                </div>
              ))}
            </div>

            <div style={{
              marginTop:24,padding:"18px 20px",borderRadius:16,
              background:"linear-gradient(135deg,#fffbeb,#fef3c7)",
              border:"1px solid #fde68a",
            }}>
              <div style={{ display:"flex",alignItems:"center",gap:8,marginBottom:8 }}>
                <span style={{ fontSize:20 }}>💡</span>
                <strong style={{ color:"#92400e",fontSize:14 }}>याद रखें</strong>
              </div>
              <p style={{ fontSize:13,margin:0,lineHeight:2,color:"#78350f" }}>
                बंधुआ मजदूरी, बाल श्रम, या शारीरिक शोषण में तुरंत पुलिस (100) या
                चाइल्ड हेल्पलाइन (1098) कॉल करें। पहचान गोपनीय रखी जाएगी।
              </p>
            </div>
          </div>
        )}
      </main>

      {/* ══════ FOOTER ══════ */}
      <footer style={{
        textAlign:"center",padding:"24px 16px 32px",position:"relative",zIndex:1,
        borderTop:"1px solid rgba(194,149,106,0.1)",
      }}>
        <div style={{ display:"flex",justifyContent:"center",gap:6,marginBottom:10 }}>
          <div style={{ width:20,height:3,borderRadius:2,background:"#FF9933" }} />
          <div style={{ width:20,height:3,borderRadius:2,background:"#fff",border:"1px solid #ddd" }} />
          <div style={{ width:20,height:3,borderRadius:2,background:"#138808" }} />
        </div>
        <p style={{ margin:0,fontSize:13,color:"#8c7b6b",fontWeight:500 }}>⚖️ मजदूर अधिकार सहायक — हर मजदूर का साथी</p>
        <p style={{ margin:"4px 0 0",fontSize:11,color:"#b8a894" }}>यह ऐप कानूनी सलाह का विकल्प नहीं है। गंभीर मामलों में वकील से संपर्क करें।</p>
      </footer>
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════
   REUSABLE COMPONENTS
   ══════════════════════════════════════════════════════════════ */
function SectionHead({ icon, title, desc }) {
  return (
    <div style={{ marginBottom:22,display:"flex",alignItems:"flex-start",gap:14 }}>
      <span style={{
        fontSize:28,width:52,height:52,borderRadius:16,flexShrink:0,
        background:"linear-gradient(135deg,rgba(194,65,12,0.1),rgba(255,153,51,0.1))",
        display:"flex",alignItems:"center",justifyContent:"center",
      }}>{icon}</span>
      <div>
        <h2 style={{ margin:0,fontSize:20,fontWeight:900,color:"#1e2952",lineHeight:1.3 }}>{title}</h2>
        <p style={{ margin:"4px 0 0",fontSize:13,color:"#8c7b6b",lineHeight:1.5 }}>{desc}</p>
      </div>
    </div>
  );
}

function GlassCard({ children, style = {} }) {
  return (
    <div style={{
      background:"rgba(255,255,255,0.65)",backdropFilter:"blur(12px)",WebkitBackdropFilter:"blur(12px)",
      borderRadius:20,padding:"26px 22px",
      border:"1px solid rgba(194,149,106,0.1)",
      boxShadow:"0 8px 32px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02)",
      ...style,
    }}>{children}</div>
  );
}

function FormField({ label, required, children, style = {} }) {
  return (
    <label style={{ display:"flex",flexDirection:"column",gap:7,...style }}>
      <span style={{ fontSize:13,fontWeight:700,color:"#1e2952" }}>
        {label}{required && <span style={{ color:"#c2410c",marginLeft:2 }}> *</span>}
      </span>
      {children}
    </label>
  );
}

const inputStyle = {
  padding:"12px 16px",borderRadius:12,border:"1.5px solid rgba(194,149,106,0.18)",
  fontSize:14,fontFamily:"'Noto Sans Devanagari',sans-serif",
  background:"rgba(255,255,255,0.6)",outline:"none",transition:"all 0.3s",
  width:"100%",boxSizing:"border-box",
};

function Input({ value, onChange, placeholder, type = "text" }) {
  return <input className="mjr-input" type={type} value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder} style={inputStyle} />;
}

function SecBtn({ onClick, children }) {
  return (
    <button onClick={onClick} style={{
      padding:"11px 22px",background:"rgba(255,255,255,0.6)",
      color:"#c2410c",border:"1.5px solid rgba(194,65,12,0.2)",
      borderRadius:12,fontSize:13,fontWeight:700,cursor:"pointer",
      fontFamily:"inherit",backdropFilter:"blur(8px)",transition:"all 0.3s",
    }}>{children}</button>
  );
}

