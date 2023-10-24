#!/bin/bash
set -e

host="${COLLECTOR_CLICKHOUSE_HOST:-localhost}"
client="clickhouse-client --host=${host}"

$client <<-EOSQL
  create table if not exists cell_towers
  (
      radio Enum8('' = 0, 'GSM' = 2, 'UMTS' = 5, 'CDMA' = 1, 'LTE' = 3, 'NR' = 4),
      mcc           UInt16,
      net           UInt16,
      area          UInt16,
      cell          UInt64,
      unit          Int16,
      lon           Float64,
      lat           Float64,
      range         UInt32,
      samples       UInt32,
      changeable    UInt8,
      created       String,
      updated       String,
      averageSignal UInt8
  )
    ENGINE = MergeTree
    PRIMARY KEY (cell, net, area, mcc, radio)
    ORDER BY (cell, net, area, mcc, radio);

EOSQL