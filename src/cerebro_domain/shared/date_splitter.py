from datetime import date, timedelta

from pydantic import BaseModel

__all__ = ["date_splitter", "DateRange", "DateRangeId"]


class DateRangeId(BaseModel):
    type: str
    id: str


class DateRange(BaseModel):
    start: date
    end: date
    ids: list[DateRangeId]


MAX_DATE: date = date.max


def date_splitter(inputs: list[DateRange]) -> list[DateRange]:
    results = []

    if len(inputs) <= 1:
        return inputs
    
    # Sort the dates by start date
    sorted_date_ranges = sorted(inputs, key=lambda d: d.start)

    pending_date_ranges: list[DateRange] = []
    min_start_date = sorted_date_ranges[0].start
    cursor = 0
    next_start_date = min_start_date
    date_ranges_length = len(sorted_date_ranges)

    while cursor < date_ranges_length:
        next_start_date_index = cursor + 1

        if cursor >= date_ranges_length:
            break

        date_range = sorted_date_ranges[cursor]

        # Find the next start date index
        min_start_date = max(min_start_date, date_range.start)
        for i in range(next_start_date_index, date_ranges_length):
            current_date_range = sorted_date_ranges[i]
            if current_date_range.start > min_start_date:
                next_start_date_index = i
                break
        
        pending_date_ranges += [date_range for date_range in sorted_date_ranges if date_range.start == min_start_date]

        pending_date_ranges = sorted(pending_date_ranges, key=lambda s: s.end)

        next_start_date = (
            sorted_date_ranges[next_start_date_index].start if next_start_date_index < date_ranges_length else MAX_DATE
        )
        before_next_start_date = next_start_date - timedelta(days=1) if next_start_date > date.min else date.min

        if next_start_date == min_start_date:
            next_start_date = before_next_start_date = pending_date_ranges[-1].end if pending_date_ranges else None

        for dtrnge in pending_date_ranges:
            end_date = (
                min(dtrnge.end, before_next_start_date)
                if before_next_start_date and next_start_date is not MAX_DATE
                else dtrnge.end
            )
            if min_start_date > end_date:
                continue
            ids: list[DateRangeId] = sum(
                [
                    date_range.ids
                    for date_range in sorted(pending_date_ranges, key=lambda s: s.start)
                    if date_range.end >= dtrnge.end       
                ],
                []
            )
            results.append(
                DateRange(
                    ids=ids,
                    start=min_start_date,
                    end=end_date
                )
            )

            min_start_date = MAX_DATE if MAX_DATE == end_date else end_date + timedelta(days=1)

            if min_start_date == MAX_DATE:
                break

        # Jump to next start date
        cursor = next_start_date_index

        pending_date_ranges = (
            (
                [d for d in pending_date_ranges if d.end >= next_start_date and d.start < MAX_DATE]
                if next_start_date < MAX_DATE
                else []
            )
            if next_start_date
            else []
        )

    return results