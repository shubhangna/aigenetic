window.CONFIG = {
  company: {
    name: 'AIgenetic',
    legalName: 'AIgenetic (OPC) Pvt Ltd',
    tagline: 'India-focused AI voice assistants',
    description: 'AI-powered phone assistants for Indian SMEs',
    location: 'Rajiv Gandhi Infotech Park, Pune, India',
    email: 'connect@aigenetic.in',
    phoneDisplay: '+91 88263 23693',
    phoneDial: '+918826323693',
    whatsappNumber: '918826323693'
  },
  hero: {
    badge: 'Live AI Assistants Handling Calls Now [V 1.19 Live]',
    heading: 'The Voice of Your Business',
    subheading: 'Never miss a customer call again. AIgenetic answers, understands, and books appointments automatically for your business—in Indian languages.',
    ctaPrimary: '📞 Book Free Demo',
    ctaSecondary: '💬 WhatsApp Us',
    trust: {
      title: 'Trusted by 100+ Indian Businesses',
      subtitle: 'Clinics, Salons, Real Estate, and more'
    },
    keyFeatures: [
      { title: 'Quick setup', subtitle: 'Get started in 48-72 hours' },
      { title: '31+ Languages', subtitle: 'Understands local accents' },
      { title: 'Works 24/7', subtitle: 'Never miss a call' },
      { title: 'Pay per use', subtitle: 'Affordable pricing' }
    ]
  },
  howItWorks: [
    { icon: '📞', step: '1', title: 'Customer Calls', desc: 'Customer dials your business number', color: 'from-blue-500 to-indigo-500' },
    { icon: '🤖', step: '2', title: 'AI Answers', desc: 'AI voice assistant answers instantly', color: 'from-indigo-500 to-purple-500' },
    { icon: '🧠', step: '3', title: 'Understands Intent', desc: "AI understands the customer's request in their language", color: 'from-purple-500 to-pink-500' },
    { icon: '📅', step: '4', title: 'Takes Action', desc: 'Books appointment or answers queries', color: 'from-pink-500 to-rose-500' },
    { icon: '✅', step: '5', title: 'Confirms', desc: 'Confirms booking and ends call', color: 'from-rose-500 to-red-500' }
  ],
  useCases: [
    { icon: '🏥', title: 'Clinics & Doctors', desc: 'Appointment booking, rescheduling, follow-ups', features: ['24/7 booking', 'Patient reminders', 'Prescription follow-ups'], gradient: 'from-blue-500 to-cyan-500' },
    { icon: '💇', title: 'Salons & Spas', desc: 'Service bookings, offers, cancellations', features: ['Service bookings', 'Package promotions', 'Membership renewals'], gradient: 'from-pink-500 to-rose-500' },
    { icon: '🏢', title: 'Real Estate', desc: 'Site visit scheduling, lead capture', features: ['Site visit booking', 'Lead qualification', 'Property inquiries'], gradient: 'from-orange-500 to-amber-500' },
    { icon: '🏫', title: 'Offices & Schools', desc: 'Enquiry handling, information desk', features: ['Admission inquiries', 'Information desk', 'Parent communication'], gradient: 'from-purple-500 to-indigo-500' }
  ],
  usps: [
    { icon: '🛠️', title: 'Fully Managed', desc: 'We handle everything from setup to maintenance', gradient: 'from-blue-500 to-indigo-500' },
    { icon: '🗣️', title: '31+ Languages', desc: 'Understands major Indian languages and accents', gradient: 'from-green-500 to-emerald-500' },
    { icon: '⏱️', title: 'Works 24/7', desc: 'Never miss a call, even on holidays', gradient: 'from-purple-500 to-pink-500' },
    { icon: '💸', title: 'Affordable', desc: 'Pay-per-use pricing for small businesses', gradient: 'from-orange-500 to-red-500' }
  ],
  testimonials: [
    { quote: "AIgenetic has been a game-changer. We don't miss appointments anymore, and patients love the 24/7 booking facility.", name: 'Dr. Priya Sharma', role: 'Skin Clinic, Mumbai' },
    { quote: 'The bot handles Hindi and Marathi perfectly. Our booking rate increased by 40% in just 2 months!', name: 'Rahul Desai', role: 'Salon Owner, Pune' },
    { quote: 'Best investment we made. Saves us ₹25,000/month compared to hiring a receptionist. Plus it never takes a day off!', name: 'Anjali Reddy', role: 'Real Estate Agency, Bangalore' }
  ],
  stats: [
    { number: '10,000+', label: 'Calls Handled', color: 'from-blue-50 to-indigo-50 border-blue-100 text-indigo-600' },
    { number: '95%', label: 'Booking Success', color: 'from-green-50 to-emerald-50 border-green-100 text-green-600' },
    { number: '2 min', label: 'Avg Call Duration', color: 'from-purple-50 to-pink-50 border-purple-100 text-purple-600' },
    { number: '100+', label: 'Happy Businesses', color: 'from-orange-50 to-amber-50 border-orange-100 text-orange-600' }
  ],
  pricingMeta: {
    setupFeeINR: 10000,
    perCallINR: 4
  },
  pricing: [
    {
      name: 'Flex',
      price: '₹4,999',
      period: '/month',
      usage: '+ ₹4 per call',
      perCallINR: 4,
      features: [
        'One-time setup (₹10,000)',
        'Dedicated phone number',
        'AI voice agent configured',
        'Appointment booking',
        'Basic analytics',
        'Email support'
      ],
      cta: 'Get Started',
      highlighted: false
    },
    {
      name: 'Pro',
      price: '₹9,999',
      period: '/month',
      usage: '+ ₹4 per call',
      perCallINR: 4,
      badge: 'Most Popular',
      features: [
        'Everything in Flex',
        'Outbound calling campaigns',
        'Advanced analytics',
        'Custom conversation flows',
        'Priority WhatsApp support',
        'Monthly optimization calls'
      ],
      cta: 'Get Started',
      highlighted: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: '',
      usage: 'Volume-based per-call pricing',
      features: [
        'Everything in Pro',
        'Multiple phone numbers',
        'API access & integrations',
        'White-label option',
        'Dedicated account manager',
        '24/7 priority support'
      ],
      cta: 'Contact Sales',
      highlighted: false
    }
  ],
  ctaMessages: {
    pricingHelp: {
      title: 'Need help choosing?',
      description: "Book a free demo and we'll recommend the best plan based on your monthly call volume. Most businesses save 60-70% compared to hiring a receptionist."
    },
    demoForm: {
      heading: 'Get Your AI Phone Assistant Live in 48-72 Hours 🚀',
      subheading: "Tell us about your business and we'll set up a personalized demo",
      responseTime: "We'll respond within 2 hours during business hours"
    }
  }
};