# Iterative DNS Resolver & HTTP Client in Python

A low-level networking client, built from scratch in Python, that performs an iterative DNS resolution for a given hostname and then uses the resulting IP address to make a basic HTTP GET request. This project was developed to demonstrate a fundamental understanding of core internet protocols without the use of simplifying libraries.

## Key Features

*   **Packet Crafting from Scratch:** DNS query packets are manually constructed by packing header and question fields into byte-level representations, ensuring 100% compliance with the relevant sections of RFC 1035.
*   **Iterative Resolution Logic:** The client correctly queries root, TLD, and authoritative DNS servers in sequence using low-level UDP sockets to resolve a hostname to its final IP address.
*   **Robust Client Behavior:** Implements a 10-second timeout mechanism to handle unresponsive DNS servers, a critical feature for real-world network reliability.
*   **Low-Level Socket Programming:** Uses only Python's standard `socket` library for all network communication, explicitly avoiding high-level libraries like `gethostbyname` or `requests`.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TysonTien0111/Iterative-DNS-Resolver-HTTP-Client.git
    cd Iterative-DNS-Resolver-HTTP-Client
    ```

2.  **Execute the client:**
    The script is configured to resolve `wikipedia.org`.
    ```bash
    python DNS_client.py
    ```

## Technologies Used

*   **Language:** Python
*   **Libraries:** `socket`, `struct`, `dataclasses`
*   **Protocols:** DNS, HTTP, UDP, TCP/IP
