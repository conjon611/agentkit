import { sendAnalyticsEvent } from "../analytics";
import { Network } from "../network";
import { WalletProvider } from "./walletProvider";

jest.mock("../analytics", () => ({
  sendAnalyticsEvent: jest.fn(),
}));

const mockSendAnalyticsEvent = sendAnalyticsEvent as jest.MockedFunction<typeof sendAnalyticsEvent>;

/**
 * Minimal concrete WalletProvider used to exercise the base class constructor.
 */
class TestWalletProvider extends WalletProvider {
  /**
   * Gets the address of the wallet.
   *
   * @returns The wallet address.
   */
  getAddress(): string {
    return "0x1234567890123456789012345678901234567890";
  }

  /**
   * Gets the network of the wallet.
   *
   * @returns The network.
   */
  getNetwork(): Network {
    return { protocolFamily: "evm", networkId: "base-sepolia", chainId: "84532" };
  }

  /**
   * Gets the name of the wallet provider.
   *
   * @returns The provider name.
   */
  getName(): string {
    return "test_wallet_provider";
  }

  /**
   * Gets the balance of the wallet.
   *
   * @returns The balance.
   */
  async getBalance(): Promise<bigint> {
    return 0n;
  }

  /**
   * Transfers the native asset.
   *
   * @returns The transaction hash.
   */
  async nativeTransfer(): Promise<string> {
    return "0xhash";
  }
}

describe("WalletProvider initialization analytics", () => {
  let warnSpy: jest.SpyInstance;

  beforeEach(() => {
    jest.clearAllMocks();
    warnSpy = jest.spyOn(console, "warn").mockImplementation(() => {});
  });

  afterEach(() => {
    warnSpy.mockRestore();
  });

  it("should report initialization", async () => {
    mockSendAnalyticsEvent.mockResolvedValue(undefined);

    new TestWalletProvider();
    await new Promise(resolve => setImmediate(resolve));

    expect(mockSendAnalyticsEvent).toHaveBeenCalledWith(
      expect.objectContaining({
        action: "initialize_wallet_provider",
        component: "wallet_provider",
        wallet_provider: "test_wallet_provider",
      }),
    );
    expect(warnSpy).not.toHaveBeenCalled();
  });

  it("should swallow a rejected analytics call rather than surfacing an unhandled rejection", async () => {
    const error = new Error("HTTP error! status: 400");
    mockSendAnalyticsEvent.mockRejectedValue(error);

    const unhandled = jest.fn();
    process.once("unhandledRejection", unhandled);

    new TestWalletProvider();
    await new Promise(resolve => setImmediate(resolve));

    process.removeListener("unhandledRejection", unhandled);

    expect(unhandled).not.toHaveBeenCalled();
    expect(warnSpy).toHaveBeenCalledWith("Failed to track wallet provider initialization:", error);
  });
});
