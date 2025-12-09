// src/components/Sidebar.tsx
const FilterSection = ({ title, items }: { title: string, items: string[] }) => (
  <div className="mb-6">
    <h3 className="font-bold text-gray-800 mb-3 text-sm">{title}</h3>
    <div className="space-y-2">
      {items.map((item, idx) => (
        <label key={idx} className="flex items-center space-x-3 cursor-pointer group">
          <div className="w-4 h-4 border border-gray-300 rounded flex items-center justify-center group-hover:border-blue-500 transition-colors">
            {/* Visual checkbox */}
          </div>
          <span className="text-sm text-gray-600 group-hover:text-gray-900">{item}</span>
        </label>
      ))}
    </div>
  </div>
);

const Sidebar = () => {
  return (
    <div className="hidden md:block w-64 bg-white p-5 rounded-xl border border-gray-100 shadow-sm h-fit sticky top-4">
      <div className="flex justify-between items-center mb-6">
        <h2 className="font-bold text-lg text-gray-900">All Filters</h2>
        <span className="text-xs text-blue-600 font-bold cursor-pointer">Applied (1)</span>
      </div>
      
      <FilterSection title="Work mode" items={['Work from office', 'Remote', 'Hybrid']} />
      <FilterSection title="Experience" items={['Fresher (0-1 Years)', 'Mid-Senior (2-5 Years)', 'Senior (5+ Years)']} />
      <FilterSection title="Department" items={['Engineering - Software', 'Data Science & Analytics', 'Product Management']} />
      <FilterSection title="Salary" items={['0-3 Lakhs', '3-6 Lakhs', '6-10 Lakhs', '10+ Lakhs']} />
    </div>
  );
};

export default Sidebar;