#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination."""

import csv
from typing import List, Dict, Tuple


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the Server."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE, encoding="utf-8") as file:
                self.__dataset = list(csv.reader(file))

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Return an indexed dataset."""
        if self.__indexed_dataset is None:
            self.__indexed_dataset = {
                i: row for i, row in enumerate(self.dataset())
            }

        return self.__indexed_dataset

    def get_hyper(self, index: int = None,
                  page_size: int = 10) -> Dict:
        """Return a hypermedia page."""
        assert type(index) is int
        assert index >= 0
        assert type(page_size) is int
        assert page_size > 0

        dataset = self.dataset()

        page = dataset[index:index + page_size]

        return {
            "index": index,
            "next_index": index + page_size
            if index + page_size < len(dataset) else None,
            "page_size": len(page),
            "data": page
        }

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10) -> Dict:
        """Return a deletion-resilient hypermedia page."""
        assert type(index) is int
        assert index >= 0
        assert type(page_size) is int
        assert page_size > 0

        indexed = self.indexed_dataset()
        data = []

        i = index

        while i < len(indexed) and len(data) < page_size:
            if i in indexed:
                data.append(indexed[i])
            i += 1

        next_index = i if i < len(indexed) else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }