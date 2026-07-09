import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const StatisticsBarChart = ({ data, valueFormatter, barColor="#7fc8a9", }) => {
  const chartData = data.map((item) => ({
    label: item[0],
    value: Number(item[1]),
  }));

  return (
    <div style={{ width: "100%", height: 260 }}>
      <ResponsiveContainer>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis allowDecimals={false} />
          <Tooltip
            formatter={(value) =>
              valueFormatter ? valueFormatter(value) : value
            }
          />
          <Bar dataKey="value" fill={barColor} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default StatisticsBarChart;
