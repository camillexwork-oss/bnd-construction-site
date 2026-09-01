/* ============================================================
   BND Construction — project data

   Source: BND's own "Company Info 2026" document (project names,
   locations, scopes and square footage) plus their project
   photography. Nothing invented. Projects with photo:false render
   as a text entry on Our Projects until photography arrives.

   TO ADD A PROJECT: copy a block, fill it in, drop a photo at
   images/projects/<slug>.jpg (900px wide) and
   images/projects/<slug>-lg.jpg (1800px wide), then re-run build.py.
   ============================================================ */
window.BND_PROJECTS = [

  /* ---------- restaurant & food service ---------- */
  {
    slug: 'walk-ons-sports-bistreaux',
    name: "Walk-On's Sports",
    market: 'Restaurant & food service',
    scope: 'New construction',
    location: 'Conroe, TX',
    status: 'Complete',
    photo: true,
    alt: "Interior bar and dining room at Walk-On's Sports, with exposed steel, brick archways and a full-length bar"
  },
  {
    slug: 'pluckers',
    name: 'Pluckers Wing Bar',
    market: 'Restaurant & food service',
    scope: 'Interior build-out',
    location: 'Addison, TX',
    status: 'Complete',
    photo: true,
    alt: 'Pluckers Wing Bar interior with brick walls, wall-mounted screens and a service counter'
  },
  {
    slug: 'fire-bowl-cafe',
    name: 'Fire Bowl Café',
    market: 'Restaurant & food service',
    scope: 'Interior remodel',
    location: 'McKinney, TX',
    status: 'Complete',
    photo: true,
    alt: 'Fire Bowl Café dining room with timber tables, pendant lighting and an open service counter'
  },
  {
    slug: 'panera-bread',
    name: 'Panera Bread',
    market: 'Restaurant & food service',
    scope: 'Interior build-out',
    location: 'Wichita Falls, TX',
    status: 'Complete',
    photo: true,
    alt: 'Panera Bread dining room with pendant lighting, timber banquettes and a tiled service counter'
  },
  {
    slug: 'oc-burger',
    name: 'OC Burger',
    market: 'Restaurant & food service',
    scope: 'Interior & exterior remodel',
    location: 'Watauga, TX',
    status: 'Complete',
    photo: true,
    alt: 'OC Burger exterior with horizontal timber cladding and a recessed entry canopy'
  },
  {
    slug: 'zukku-sushi',
    name: 'Zukku Sushi',
    market: 'Restaurant & food service',
    scope: 'Interior build-out',
    location: 'Allen, TX',
    status: 'Under construction',
    photo: false
  },
  {
    slug: 'andys-frozen-custard',
    name: "Andy's Frozen Custard",
    market: 'Restaurant & food service',
    scope: 'New construction',
    location: 'San Antonio, TX',
    status: 'Complete',
    photo: true,
    alt: "Andy's Frozen Custard exterior with a red and white drive-thru canopy, menu boards and stone-clad servery"
  },

  /* ---------- retail ---------- */
  {
    slug: 'ralph-lauren-northpark',
    name: 'Ralph Lauren',
    market: 'Retail',
    scope: 'Interior remodel',
    location: 'NorthPark Mall, Dallas, TX',
    status: 'Complete',
    photo: true,
    alt: 'Ralph Lauren store interior with tailored menswear, timber floors and white display joinery'
  },
  {
    slug: 'celine-highland-park-village',
    name: 'Celine',
    market: 'Retail',
    scope: 'Interior build-out',
    location: 'Highland Park Village, TX',
    status: 'Complete',
    photo: true,
    alt: 'Celine boutique interior with handbags on backlit shelving and a stone plinth display'
  },
  {
    slug: 'massage-luxe',
    name: 'MassageLuXe',
    market: 'Retail',
    scope: 'Interior build-out',
    location: 'Frisco & Wylie, TX',
    status: 'Complete',
    photo: true,
    alt: 'MassageLuXe reception with a stone feature wall, custom desk and graphic wall treatment'
  },
  {
    slug: 'oak-point',
    name: 'Duncanville Shopping Center',
    market: 'Retail',
    scope: 'New construction — 28,000 SF',
    location: 'Oak Point, TX',
    status: 'Complete',
    photo: true,
    alt: 'Duncanville Shopping Center photographed at dusk, with a stucco parapet and colonnade'
  },
  {
    slug: 'beem-light-sauna',
    name: 'Beem Light Sauna',
    market: 'Retail',
    scope: 'Interior build-out',
    location: 'Addison, TX',
    status: 'Complete',
    photo: true,
    alt: 'Beem Light Sauna reception in white joinery with a rounded ceiling detail'
  },
  {
    slug: 'prosper-retail-shell',
    name: 'Prosper Retail Shell',
    market: 'Retail',
    scope: 'New construction — 13,900 SF',
    location: 'Prosper, TX',
    status: 'Under construction',
    photo: true,
    alt: 'Prosper Retail Shell under construction — timber framing and structural steel being set by crane over a poured slab'
  },

  /* ---------- medical & dental ---------- */
  {
    slug: 'evolve-dermatology',
    name: 'Evolve Dermatology',
    market: 'Medical & dental',
    scope: 'Additions & renovation — 3,712 SF',
    location: 'Forney, TX',
    status: 'Complete',
    photo: true,
    alt: 'Evolve Dermatology clinic exterior in stone and glass with a full-height curtain wall'
  },
  {
    slug: 'bear-family-dental',
    name: 'Bear Family Dental',
    market: 'Medical & dental',
    scope: 'New construction — 11,000 SF',
    location: 'Grapevine, TX',
    status: 'Complete',
    photo: true,
    alt: 'Bear Family Dental building exterior in light masonry with a dark storefront system'
  },

  /* ---------- education ---------- */
  {
    slug: 'excellence-academy-montessori',
    name: 'Excellence Academy Montessori — Five Buildings',
    market: 'Education',
    scope: 'New construction — 34,000 SF',
    location: 'McKinney, TX',
    status: 'Under construction',
    photo: true,
    alt: 'Site plan for the Excellence Academy Montessori campus, showing the five buildings, playing fields and parking'
  },
  {
    slug: 'arlington-early-college',
    name: 'Arlington Early College',
    market: 'Education',
    scope: 'Interior finish-out',
    location: 'Arlington, TX',
    status: 'Complete',
    /* NOTE: the only available image is a 299x168 thumbnail from the company
       profile. It is upscaled here and looks soft — replace with a real photo
       before launch if BND can supply one. */
    photo: true,
    alt: 'Arlington Early College exterior with a blue metal fascia, glazed classrooms and a cable balustrade'
  },

  /* ---------- multifamily ---------- */
  {
    slug: 'villa-at-vanston',
    name: 'Villa at Vanston — 176 Units',
    market: 'Multifamily',
    scope: 'New construction',
    location: 'Mesquite, TX',
    status: 'Complete',
    photo: true,
    alt: 'Villa at Vanston multifamily building in brick with projecting balconies'
  },

  /* ---------- convenience & fuel ---------- */
  {
    slug: 'mateos-gas-station',
    name: "Mateo's Gas Station",
    market: 'Convenience & fuel',
    scope: 'New construction',
    location: 'Fort Worth, TX',
    status: 'Complete',
    photo: false
  },
  {
    slug: 'gas-station-fuel',
    name: 'H Express',
    market: 'Convenience & fuel',
    scope: 'New construction',
    location: null,
    status: 'Complete',
    photo: true,
    alt: 'H Express convenience store exterior in stone and stucco with red awnings'
  },
  {
    slug: 'travel-center-tonkawa',
    name: 'Travel Center',
    market: 'Convenience & fuel',
    scope: 'New construction',
    location: '16700 W South Ave, Tonkawa, OK',
    status: 'Complete',
    photo: false
  },
  {
    slug: 'cstore-houston-montgomery',
    name: 'C-Store with Fuel',
    market: 'Convenience & fuel',
    scope: 'New construction',
    location: '7701 W Montgomery Rd, Houston, TX',
    status: 'Complete',
    photo: false
  },
  {
    slug: 'cstore-hankamer',
    name: 'C-Store with Fuel',
    market: 'Convenience & fuel',
    scope: 'New construction',
    location: '36311 I-10, Hankamer, TX',
    status: 'Complete',
    photo: false
  }
];
