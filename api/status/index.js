// api/status/index.js (Versi Super Solid)

// 'Database' sederhana kita di memori server
let systemStatus = {
  last_updated: null,
  components: {
    termux_agent: { status: 'offline', cycles: 0, last_seen: null },
    code_guardian: { status: 'idle', result: 'unknown', last_run: null },
    quantum_pipeline: { status: 'idle', result: 'unknown', last_run: null },
    business_insight: { status: 'idle', result: 'unknown', last_run: null },
    evolution_chamber: { status: 'idle', result: 'unknown', last_run: null },
    self_healing: { status: 'idle', result: 'unknown', last_run: null }
  }
};

export default function handler(req, res) {
  // Izinkan koneksi dari mana saja (CORS)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method === 'POST') {
    const { component, status, data } = req.body;
    if (component && systemStatus.components[component]) {
      systemStatus.components[component].status = status;
      systemStatus.components[component].last_seen = new Date().toISOString();
      Object.assign(systemStatus.components[component], data); // Gabungkan data tambahan
      systemStatus.last_updated = new Date().toISOString();
      
      return res.status(200).json({ message: `Status for ${component} updated.` });
    }
    return res.status(400).json({ error: 'Invalid component.' });
  } 
  
  if (req.method === 'GET') {
    // Tambahkan header anti-cache
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    
    return res.status(200).json(systemStatus);
  }
  
  return res.status(405).json({ error: 'Method Not Allowed' });
}
