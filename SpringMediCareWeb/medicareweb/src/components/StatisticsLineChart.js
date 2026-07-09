import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const StatisticsLineChart = ({ data, valueFormatter }) => {
  const chartData = data.map((item) => ({
    label: `Tháng ${item[0]}`,
    value: Number(item[1]),
  }));

  return (
    <div style={{ width: "100%", height: 260 }}>
      <ResponsiveContainer>
        <LineChart
          data={chartData}
          margin={{ top: 10, right: 20, left: 35, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis
            width={90}
            tickFormatter={(value) => Number(value).toLocaleString("vi-VN")}
          />
          <Tooltip
            formatter={(value) =>
              valueFormatter ? valueFormatter(value) : value
            }
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#4aaedf"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default StatisticsLineChart;
