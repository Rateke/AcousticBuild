import { useState } from 'react';
import Header from '../components/Header';
import ScrollVideoBackground from '../components/ScrollVideoBackground';
import HeroSection from '../components/HeroSection';
import WhatWeAreSection from '../components/WhatWeAreSection';
import ProductSection from '../components/ProductSection';
import WhoWeAreSection from '../components/WhoWeAreSection';

import AccessCalculatorButton from '../components/AccessCalculatorButton';
import Footer from '../components/Footer';
import Sidebar from '../components/Sidebar';

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <>
      <ScrollVideoBackground />
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <Header onMenuClick={() => setSidebarOpen(true)} />
      <HeroSection />
      <section id="o-que-somos">
        <WhatWeAreSection />
      </section>
      <section id="produto">
        <ProductSection />
        <AccessCalculatorButton />
      </section>
      <section id="quem-somos">
        <WhoWeAreSection />
      </section>
      <Footer />
    </>
  );
}
