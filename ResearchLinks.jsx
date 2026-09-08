import React from 'react'

// Live research quick-links — query = primary scripture if set, otherwise topic.
// Opens each source in a new tab; nothing is submitted anywhere.

export default function ResearchLinks({ scripture, topic }) {
  const q = (scripture || '').trim() || (topic || '').trim()
  if (!q) return null

  const enc = encodeURIComponent(q)
  const links = [
    {
      label: '📖 BibleGateway',
      url: `https://www.biblegateway.com/passage/?search=${enc}&version=NIV`,
      hint: 'Full passage + cross translations',
    },
    {
      label: '🔤 BibleHub',
      url: `https://biblehub.com/search?q=${enc}`,
      hint: 'Hebrew/Greek, interlinear, commentaries',
    },
    {
      label: '🎓 Google Scholar',
      url: `https://scholar.google.com/scholar?q=${enc}`,
      hint: 'Academic / scholarly sources',
    },
    {
      label: '🌐 Google',
      url: `https://www.google.com/search?q=${enc}`,
      hint: 'General context + alternative views',
    },
  ]

  return (
    <div style={{marginTop:20, padding:16, background:'var(--surface-2)', borderRadius:8}}>
      <div style={{fontWeight:600, marginBottom:4}}>Research "{q}"</div>
      <div style={{color:'var(--text-muted)', fontSize:'0.8125rem', marginBottom:12}}>
        Opens in a new tab. Gather context, original language, and sources — then fill the fields below.
      </div>
      <div style={{display:'flex', gap:8, flexWrap:'wrap'}}>
        {links.map(l => (
          <a
            key={l.label}
            href={l.url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-outline"
            style={{fontSize:'0.8125rem', textDecoration:'none'}}
            title={l.hint}
          >
            {l.label}
          </a>
        ))}
      </div>
    </div>
  )
}
