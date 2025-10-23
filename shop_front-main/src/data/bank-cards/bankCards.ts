import ansar from '@/assets/image/banks/ansar-05.svg';
import ayandeh from '@/assets/image/banks/ayande-03.svg';
import dey from '@/assets/image/banks/day-12.svg';
import eghtesad from '@/assets/image/banks/eghtesad-04.svg';
import tosee from '@/assets/image/banks/tose-11.svg';
import gardeshgari from '@/assets/image/banks/gardeshgari-20.svg';
import ghavvamin from '@/assets/image/banks/ghavvamin-31.svg';
import karafarin from '@/assets/image/banks/karafarin-06.svg';
import keshavarzi from '@/assets/image/banks/keshavarzi-07.svg';
import maskan from '@/assets/image/banks/maskan-26.svg';
import mehrEghtesad from '@/assets/image/banks/mehreghtesad-14.svg';
import mehrIranian from '@/assets/image/banks/mehriran-15.svg';
import melli from '@/assets/image/banks/melli-22.svg';
import mellat from '@/assets/image/banks/mellat-02.svg';
import shetab from '@/assets/image/banks/shetab.svg';
import pasargad from '@/assets/image/banks/pasargad-10.svg'
import post from '@/assets/image/banks/post-09.svg'
import refah from '@/assets/image/banks/refahkargaran-28.svg'
import sanatmadan from '@/assets/image/banks/sanatmadan-16.svg'
import saderat from '@/assets/image/banks/saderat-29.svg'
import saman from '@/assets/image/banks/saman-01.svg'
import sarmaye from '@/assets/image/banks/sarmaye-17.svg'
import sepah from '@/assets/image/banks/sepah-24.svg'
import shahr from '@/assets/image/banks/shahr-25.svg'
import sina from '@/assets/image/banks/sina-23.svg'
import tejarat from '@/assets/image/banks/tejarat-13.svg'
import hekmat from '@/assets/image/banks/hekmat-30.svg'
import toseeSaderat from '@/assets/image/banks/tosesaderat-18.svg'
import toseeTaavon from '@/assets/image/banks/tosetaavon-19.svg'

export interface BankCard {
    card_no: number,
    bank_name: string,
    bank_title: string,
    bank_logo: string,
    color: string
}

export const bankCards: BankCard[] = [
    {
        card_no: 627381,
        bank_name: 'ansar',
        bank_title: 'بانک انصار',
        bank_logo: ansar,
        color: '#26eeb900'
    },
    {
        card_no: 636214,
        bank_name: 'ayandeh',
        bank_title: 'بانک آینده',
        bank_logo: ayandeh,
        color: '#3388391d'
    },
    {
        card_no: 502938,
        bank_name: 'dey',
        bank_title: 'بانک دی',
        bank_logo: dey,
        color: '#0dffffff'
    },
    {
        card_no: 627412,
        bank_name: 'eghtesad_novin',
        bank_title: 'بانک اقتصادنوین',
        bank_logo: eghtesad,
        color: '#1a662891'
    },
    {
        card_no: 628157,
        bank_name: 'etebari_tosee',
        bank_title: 'موسسه اعتباری توسعه',
        bank_logo: tosee,
        color: '#33000000'
    },
    {
        card_no: 505416,
        bank_name: 'gardeshgari',
        bank_title: 'بانک گردشگری',
        bank_logo: gardeshgari,
        color: '#29344143'
    },
    {
        card_no: 639599,
        bank_name: 'ghavvamin',
        bank_title: 'بانک قوامین',
        bank_logo: ghavvamin,
        color: '#1afff400'
    },
    {
        card_no: 627488,
        bank_name: 'kar_afarin',
        bank_title: 'بانک کارآفرین',
        bank_logo: karafarin,
        color: '#333a881d'
    },
    {
        card_no: 502910,
        bank_name: 'kar_afarin',
        bank_title: 'بانک کارآفرین',
        bank_logo: karafarin,
        color: '#333a881d'
    },
    {
        card_no: 603770,
        bank_name: 'keshavarzi',
        bank_title: 'بانک کشاورزی',
        bank_logo: keshavarzi,
        color: '#29aa9a22'
    },
    {
        card_no: 639217,
        bank_name: 'keshavarzi',
        bank_title: 'بانک کشاورزی',
        bank_logo: keshavarzi,
        color: '#29aa9a22'
    },
    {
        card_no: 628023,
        bank_name: 'maskan',
        bank_title: 'بانک مسکن',
        bank_logo: maskan,
        color: '#1a000000'
    },
    {
        card_no: 639370,
        bank_name: 'mehr_e_eghtesad',
        bank_title: 'بانک مهر اقتصاد',
        bank_logo: mehrEghtesad,
        color: '#1a656565'
    },
    {
        card_no: 606373,
        bank_name: 'mehr_e_iranian',
        bank_title: 'بانک قرض الحسنه مهر ایرانیان',
        bank_logo: mehrIranian,
        color: '#1a209b1c'
    },
    {
        card_no: 603799,
        bank_name: 'meli',
        bank_title: 'بانک ملی ایران',
        bank_logo: melli,
        color: '#1a00e0d7'
    },
    {
        card_no: 610433,
        bank_name: 'mellat',
        bank_title: 'بانک ملت',
        bank_logo: mellat,
        color: '#1aba0b22'
    },
    {
        card_no: 991975,
        bank_name: 'mellat',
        bank_title: 'بانک ملت',
        bank_logo: mellat,
        color: '#1aba0b22'
    },
    {
        card_no: 111111,
        bank_name: 'ok',
        bank_title: 'همه کارتخوان‌ها',
        bank_logo: shetab,
        color: '#1a00e0d7'
    },
    {
        card_no: 502229,
        bank_name: 'pasargad',
        bank_title: 'بانک پاسارگاد',
        bank_logo: pasargad,
        color: '#4d000000'
    },
    {
        card_no: 639347,
        bank_name: 'pasargad',
        bank_title: 'بانک پاسارگاد',
        bank_logo: pasargad,
        color: '#4d000000'
    },
    {
        card_no: 627760,
        bank_name: 'post_bank',
        bank_title: 'پست بانک ایران',
        bank_logo: post,
        color: '#1a14763e'
    },
    {
        card_no: 589463,
        bank_name: 'refah',
        bank_title: 'بانک رفاه',
        bank_logo: refah,
        color: '#0d000000'
    },
    {
        card_no: 627961,
        bank_name: 'saanat_va_maadan',
        bank_title: 'بانک صنعت و معدن',
        bank_logo: sanatmadan,
        color: '#339b814c'
    },
    {
        card_no: 603769,
        bank_name: 'saderat',
        bank_title: 'بانک صادرات',
        bank_logo: saderat,
        color: '#004ec2'
    },
    {
        card_no: 621986,
        bank_name: 'saman',
        bank_title: 'بانک سامان',
        bank_logo: saman,
        color: '#1a7dcdf1'
    },
    {
        card_no: 639607,
        bank_name: 'sarmayeh',
        bank_title: 'بانک سرمایه',
        bank_logo: sarmaye,
        color: '#29bd9ff5'
    },
    {
      card_no: 589210,
       bank_name: 'sepah',
        bank_title: 'بانک سپه',
        bank_logo: sepah,
        color: '#33ffc400'
    },
    {
        card_no: 504706,
        bank_name: 'shahr',
        bank_title: 'بانک شهر',
        bank_logo: shahr,
        color: '#29ffafb2'
    },
    {
        card_no: 502806,
        bank_name: 'shahr',
        bank_title: 'بانک شهر',
        bank_logo: shahr,
        color: '#29ffafb2'
    },
    {
        card_no: 639346,
        bank_name: 'sina',
        bank_title: 'بانک سینا',
        bank_logo: sina,
        color: '#1a277eb5'
    },
    {
        card_no: 627353,
        bank_name: 'tejarat',
        bank_title: 'بانک تجارت',
        bank_logo: tejarat,
        color: '#290fadc7'
    },
    {
        card_no: 585983,
        bank_name: 'tejarat',
        bank_title: 'بانک تجارت',
        bank_logo: tejarat,
        color: '#290fadc7'
    },
    {
        card_no: 636949,
        bank_name: 'tejarat',
        bank_title: 'بانک حکمت',
        bank_logo: hekmat,
        color: '#29563288'
    },
    {
        card_no: 627648,
        bank_name: 'tosee_saderat',
        bank_title: 'بانک توسعه صادرات',
        bank_logo: toseeSaderat,
        color: '#1f6d6900'
    },
    {
        card_no: 502908,
        bank_name: 'tosee_taavon',
        bank_title: 'بانک توسعه تعاون',
        bank_logo: toseeTaavon,
        color: '#290076ff'
    }
];