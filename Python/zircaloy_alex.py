m_u235 = 235.04
m_u238 = 238.05

m_li6 = 6.015
m_li7 = 7.016

mu = 1.66054 # atomic mass constant 

num_u235 = 0.0008518897 # 0.00103366
num_u238 = 0.0231911372 # 0.02300490

vol_fuel = 50.2655
vol_clad = 16.7761

mass_uranium = (num_u235 * m_u235 + num_u238 * m_u238) * mu * vol_fuel

target = 70 # in milligrams per kilogram uranium

num_li6 = ((target/1000) * mass_uranium/1000)/(m_li6 * mu * vol_clad)

li_enrichment = 0.9 # in weight percent

num_li7 = num_li6 * (m_li6/m_li7) * (1 - li_enrichment) / li_enrichment

print(f'{num_li6:.10f}')
print(f'{num_li7:.10f}')