const VIETNAM_TIME_ZONE = "Asia/Ho_Chi_Minh";

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: VIETNAM_TIME_ZONE,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(date);

  const year = parts.find((part) => part.type === "year")?.value;
  const month = parts.find((part) => part.type === "month")?.value;
  const day = parts.find((part) => part.type === "day")?.value;

  if (!year || !month || !day) {
    return "";
  }

  return `${year}-${month}-${day}`;
};

export const formatScheduleDateKey = (value) => {
  if (value === null || value === undefined || value === "") {
    return "";
  }

  // API trả timestamp mili-giây, ví dụ 1785862800000
  if (typeof value === "number") {
    return formatTimestamp(value);
  }

  // API trả timestamp dưới dạng chuỗi số
  if (typeof value === "string" && /^\d{10,13}$/.test(value.trim())) {
    const numericValue = Number(value.trim());

    return formatTimestamp(
      value.trim().length === 10 ? numericValue * 1000 : numericValue,
    );
  }

  // API trả YYYY-MM-DD hoặc YYYY-MM-DDT...
  if (typeof value === "string") {
    const isoMatch = value.trim().match(/^(\d{4})-(\d{1,2})-(\d{1,2})/);

    if (isoMatch) {
      const year = isoMatch[1];
      const month = isoMatch[2].padStart(2, "0");
      const day = isoMatch[3].padStart(2, "0");

      return `${year}-${month}-${day}`;
    }
  }

  // API trả [2026, 8, 5]
  if (Array.isArray(value)) {
    const [year, month, day] = value;

    return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(
      2,
      "0",
    )}`;
  }

  // API trả object ngày
  if (typeof value === "object") {
    const year = value.year;
    const month = value.month ?? value.monthValue;
    const day = value.day ?? value.dayOfMonth;

    if (year && month && day) {
      return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(
        2,
        "0",
      )}`;
    }
  }

  return "";
};

export const parseScheduleDate = (value) => {
  const dateKey = formatScheduleDateKey(value);

  if (!dateKey) {
    return null;
  }

  return new Date(`${dateKey}T00:00:00`);
};
