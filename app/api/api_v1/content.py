import logging
import math
from os.path import exists
from typing import Dict, Optional

import pandas
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse
from starlette.responses import FileResponse
from tqdm.std import tqdm

from openeye_backend import crud, schemas
from openeye_backend.api import deps
from openeye_backend.api.api_v1.biosynth_bk_task import (
    GenerateBiosynthProductDescriptionThread,
)
from openeye_backend.api.api_v1.utils.common import (
    get_count_writing_assistant_generation_today,
    get_inputs,
    get_writing_assistant_values_per_plan,
    response_content,
)
from openeye_backend.api.api_v1.utils.diffbot_scrape import scrape_article
from openeye_backend.content.templates import (
    ads_and_marketing_tools,
    articles_and_blogs,
    ecommerce,
    general_writing,
    other,
    social_media,
    website_copy,
)

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)


router = APIRouter(prefix="/content", tags=["Content"])


@router.post("/google-ads", response_model=schemas.OutputGoogleAdList)
def google_ads(
    input_data: schemas.InputGoogleAd,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.GoogleAds(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/google-ad-titles", response_model=schemas.OutputGoogleAdTitleList)
def google_ad_titles(
    input_data: schemas.InputGoogleAdTitle,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.GoogleAdTitles(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/google-ad-descriptions", response_model=schemas.OutputGoogleAdDescriptionList
)
def google_ad_descriptions(
    input_data: schemas.InputGoogleAdDescription,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.GoogleAdDescriptions(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/facebook-ads", response_model=schemas.OutputFacebookAdList)
def facebook_ads(
    input_data: schemas.InputFacebookAd,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.FacebookAds(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/linkedin-ad-headlines", response_model=schemas.OutputLinkedinAdHeadlineList
)
def linkedin_ad_headlines(
    input_data: schemas.InputLinkedinAdHeadline,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.LinkedinAdHeadlines(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/linkedin-ad-descriptions", response_model=schemas.OutputLinkedinAdDescriptionList
)
def linkedin_ad_descriptions(
    input_data: schemas.InputLinkedinAdHeadline,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.LinkedinAdDescriptions(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/linkedin-ads", response_model=schemas.OutputLinkedinAdList)
def linkedin_ads(
    input_data: schemas.InputLinkedinAdHeadline,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.LinkedinAds(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/linkedin-posts", response_model=schemas.OutputLinkedinPostList)
def linkedin_posts(
    input_data: schemas.InputLinkedinPost,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.LinkedinPosts(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/landing-page-headlines", response_model=schemas.OutputLandingPageHeadlineList
)
def landing_page_headlines(
    input_data: schemas.InputLandingPageHeadline,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=website_copy.LandingPageHeadlines(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/landing-pages", response_model=schemas.OutputLandingPageList)
def landing_pages(
    input_data: schemas.InputLandingPage,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    if not input_data.product_description.lower().startswith(
        input_data.product_name.lower()
    ):
        raise HTTPException(
            406,
            f"Please make sure that your product/service description starts with your product/service name. For example, {input_data.product_name} is a platform that lets you...",
        )

    return response_content(
        db,
        result=website_copy.LandingPages(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/product-descriptions", response_model=schemas.OutputProductDescriptionList
)
def product_descriptions(
    input_data: schemas.InputProductDescription,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ecommerce.ProductDescriptions(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/amazon-product-descriptions",
    response_model=schemas.OutputAmazonProductDescriptionList,
)
def amazon_product_descriptions(
    input_data: schemas.InputAmazonProductDescription,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ecommerce.AmazonProductDescriptions(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/amazon-product-titles", response_model=schemas.OutputAmazonProductTitleList
)
def amazon_product_titles(
    input_data: schemas.InputAmazonProductTitle,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ecommerce.AmazonProductTitles(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/amazon-product-features", response_model=schemas.OutputAmazonProductFeatureList
)
def amazon_product_features(
    input_data: schemas.InputAmazonProductFeature,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ecommerce.AmazonProductFeatures(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/amazon-ad-headlines", response_model=schemas.OutputAmazonAdHeadlineList)
def amazon_ad_headlines(
    input_data: schemas.InputAmazonAdHeadline,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ecommerce.AmazonAdHeadlines(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/blog-ideas", response_model=schemas.OutputBlogIdeaList)
def blog_ideas(
    input_data: schemas.InputBlogIdea,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=articles_and_blogs.BlogIdeas(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/blog-intros", response_model=schemas.OutputBlogIntroList)
def blog_intros(
    input_data: schemas.InputBlogIntro,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=articles_and_blogs.BlogIntros(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/blog-outlines", response_model=schemas.OutputBlogOutlineList)
def blog_outlines(
    input_data: schemas.InputBlogOutline,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=articles_and_blogs.BlogOutlines(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/feature-to-benefits", response_model=schemas.OutputFeatureToBenefitList)
def feature_to_benefits(
    input_data: schemas.InputFeatureToBenefit,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=website_copy.FeatureToBenefits(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/content-rephrase", response_model=schemas.OutputContentRephraseList)
def content_rephrase(
    input_data: schemas.InputContentRephrase,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]

    return response_content(
        db,
        result=general_writing.ContentRephrase(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/sentence-expand", response_model=schemas.OutputSentenceExpandList)
def sentence_expand(
    input_data: schemas.InputSentenceExpand,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]

    data = response_content(
        db,
        result=general_writing.SentenceExpand(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )
    if data.copies is not None:
        data.copies.items = sorted(
            data.copies.items, key=lambda x: len(x.data["text"]), reverse=True
        )
    return data


@router.post("/content-shorten", response_model=schemas.OutputContentShortenList)
def content_shorten(
    input_data: schemas.InputContentShorten,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]

    return response_content(
        db,
        result=general_writing.ContentShorten(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/listicle-ideas", response_model=schemas.OutputListicleIdeaList)
def listicle_ideas(
    input_data: schemas.InputListicleIdea,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.ListicleIdeas(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/emails", response_model=schemas.OutputEmailList)
def emails(
    input_data: schemas.InputEmail,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.Emails(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/emails-v2", response_model=schemas.OutputEmailV2List)
def emails_v2(
    input_data: schemas.InputEmailV2,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.EmailsV2(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/growth-ideas", response_model=schemas.OutputGrowthIdeaList)
def growth_ideas(
    input_data: schemas.InputGrowthIdea,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.GrowthIdeas(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/startup-ideas", response_model=schemas.OutputStartupIdeaList)
def startup_ideas(
    input_data: schemas.InputStartupIdea,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.StartupIdeas(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/pas", response_model=schemas.OutputPasList)
def pas(
    input_data: schemas.InputPas,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.Pas(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/aida", response_model=schemas.OutputAidaList)
def aida(
    input_data: schemas.InputAida,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.Aida(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/meta-home", response_model=schemas.OutputMetaHomeList)
def seo_meta_tags_home(
    input_data: schemas.InputMetaHome,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=website_copy.MetaHome(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/meta-blog", response_model=schemas.OutputMetaBlogList)
def seo_meta_tags_blog(
    input_data: schemas.InputMetaBlog,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=website_copy.MetaBlog(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/meta-prod", response_model=schemas.OutputMetaProdList)
def seo_meta_tags_product(
    input_data: schemas.InputMetaProd,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=website_copy.MetaProd(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/youtube-titles", response_model=schemas.OutputYoutubeTitleList)
def youtube_titles(
    input_data: schemas.InputYoutubeTitle,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.YoutubeTitles(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/youtube-ideas", response_model=schemas.OutputYoutubeIdeaList)
def youtube_ideas(
    input_data: schemas.InputYoutubeIdea,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.YoutubeIdeas(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/youtube-outlines", response_model=schemas.OutputYoutubeOutlineList)
def youtube_outlines(
    input_data: schemas.InputYoutubeOutline,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.YoutubeOutlines(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/youtube-descriptions", response_model=schemas.OutputYoutubeDescriptionList
)
def youtube_descriptions(
    input_data: schemas.InputYoutubeDescription,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.YoutubeDescriptions(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/youtube-intros", response_model=schemas.OutputYoutubeIntroList)
def youtube_intros(
    input_data: schemas.InputYoutubeIntro,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.YoutubeIntros(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/keyword-extract", response_model=schemas.OutputKeywordExtractList)
def keyword_extract(
    input_data: schemas.InputKeywordExtract,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.KeywordExtract(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/product-names", response_model=schemas.OutputProductNameList)
def product_names(
    input_data: schemas.InputProductName,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.ProductNames(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/analogies", response_model=schemas.OutputAnalogyList)
def analogies(
    input_data: schemas.InputAnalogy,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.Analogies(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/short-press-releases", response_model=schemas.OutputShortPressReleaseList
)
def short_press_releases(
    input_data: schemas.InputShortPressRelease,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.ShortPressReleases(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/company-bios", response_model=schemas.OutputCompanyBioList)
def company_bios(
    input_data: schemas.InputCompanyBio,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.CompanyBios(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/company-vision", response_model=schemas.OutputCompanyVisionList)
def company_vision(
    input_data: schemas.InputCompanyVision,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.CompanyVision(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/company-mission", response_model=schemas.OutputCompanyMissionList)
def company_mission(
    input_data: schemas.InputCompanyMission,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.CompanyMission(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/personal-bios", response_model=schemas.OutputPersonalBioList)
def personal_bios(
    input_data: schemas.InputPersonalBio,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.PersonalBios(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/summary", response_model=schemas.OutputSummaryList)
def summary(
    input_data: schemas.InputSummary,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.Summary(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/ai-article-writer", response_model=schemas.OutputAiArticleWriterList)
def ai_article_writer(
    input_data: schemas.InputAiArticleWriter,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=articles_and_blogs.AiArticleWriter(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/ai-article-writer-v2", response_model=schemas.OutputAiArticleWriterList)
def ai_article_writer_v2(
    input_data: schemas.InputAiArticleWriter,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=articles_and_blogs.AiArticleWriterV2(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/ai-article-writer-v3", response_model=schemas.OutputAiArticleWriterList)
def ai_article_writer_v3(
    input_data: schemas.InputAiArticleWriter,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=articles_and_blogs.AiArticleWriterV3(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.get("/writing-assistant/sse")
async def writing_assistant_sse(
    request: Request,
    seed_text: str,
    max_tokens: int,
    temperature: float,
    engine_id: Optional[str] = None,
    title: Optional[str] = "",
    description: Optional[str] = "",
    language: Optional[str] = "en",
    user_info: str = Depends(deps.get_user_info_from_param),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    props = {
        "seed_text": seed_text,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "title": title,
        "description": description,
        "language": language,
        "engine_id": engine_id,
    }
    if "admin_id" in props:
        props["admin_id"] = user_info["admin_id"]
    result = articles_and_blogs.WritingAssistant(
        props=props,
        user_id=user_id,
        db=db,
    ).generate_sse(request=request, db=db)

    return EventSourceResponse(result)


@router.get(
    "/writing-assistant/available-values",
    response_model=Optional[schemas.WritingAssistantAvailableValues],
)
def get_writing_assistant_available_values(
    user_id: str = Depends(deps.get_user_id),
    db: Session = Depends(deps.get_db),
) -> any:
    # count the generation Today
    num_used_today = get_count_writing_assistant_generation_today(db, user_id=user_id)

    # get max response length and max count of generations per day
    values_per_plan = get_writing_assistant_values_per_plan(db, user_id=user_id)
    charge_credits = values_per_plan.charge_credits
    max_response_tokens = values_per_plan.max_response_tokens
    max_generations_per_day = values_per_plan.max_generations_per_day

    return schemas.WritingAssistantAvailableValues(
        charge_credits=charge_credits,
        num_used_today=num_used_today,
        max_response_tokens=max_response_tokens,
        max_generations_per_day=max_generations_per_day,
    )


@router.post("/biosynth-product-description")
async def biosynth_product_description(
    excel_file: UploadFile = File(...),
    params=Depends(deps.get_content_parameters),
    user_info=Depends(deps.get_user_info),
    db: Session = Depends(deps.get_db),
) -> any:
    if (
        excel_file.content_type
        != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        and excel_file.content_type != "application/vnd.ms-excel"
    ):
        raise HTTPException(404, "Format is invalid")
    contents = await excel_file.read()
    xlsx = pandas.read_excel(contents, index_col=0)
    # read template file
    template_pd = pandas.read_excel(
        "public_templates/biosynth_product_description.xlsx", index_col=0
    )
    if (False in template_pd.columns == xlsx.columns) == True:
        raise HTTPException(
            404,
            "Invalid data format! Please download the template and make sure your uploaded file matches the template's format.",
        )

    if xlsx.empty == True:
        raise HTTPException(404, "The uploaded file is empty")

    charge_credits = 0.25
    count_rows = len(xlsx.index)

    # calculate total charge credits
    total_charge_credits = 0
    pbar = tqdm(xlsx.iterrows(), total=xlsx.shape[0])
    err_namproden = ""
    err_tag = ""
    for index, row in pbar:
        namproden = row["namproden"]
        if len(namproden) < 2:
            err_namproden += (", " if err_namproden != "" else "") + index + 2
        tags = row["tags"]
        if len(tags) < 2:
            err_tag += (", " if err_tag != "" else "") + index + 2

        column0 = "ai_short_description"
        column1 = "ai_product_descriptions (20% creative)"
        column2 = "ai_product_descriptions (50% creative)"
        column3 = "ai_product_descriptions (70% creative)"
        if (
            pandas.isna(row[column0])
            or pandas.isna(row[column1])
            or pandas.isna(row[column2])
            or pandas.isna(row[column3])
        ):
            total_charge_credits += charge_credits

    err_message = ""
    if err_namproden != "":
        err_message += (
            f"the cells [{err_namproden}] of namproden must have more 2 characters"
        )
    if err_tag != "":
        err_message += (
            ", " if err_message != "" else ""
        ) + f"the cells [{err_namproden}] of tags must have more 2 characters"
    if err_message != "":
        raise HTTPException(
            406,
            err_message,
        )

    total_charge_credits = charge_credits * count_rows * 4

    # check if the user has enough credits
    user_id = user_info["admin_id"] if "admin_id" in user_info else user_info["user_id"]
    if user_id is not None:
        user = crud.user.get_by_id(db, fb_id=user_id)
        if user is None:
            raise HTTPException(406, "Invalid user")
        recurring_credits = user.recurring_credits
        lifetime_deal_credits = user.lifetime_deal_credits
        one_time_credits = user.one_time_credits
        reward_credits = user.reward_credits
        if (
            recurring_credits
            + lifetime_deal_credits
            + one_time_credits
            + reward_credits
            < total_charge_credits
        ):
            raise HTTPException(
                406,
                f"You need {math.ceil(total_charge_credits)} credits at least. Please purchase credits.",
            )
    GenerateBiosynthProductDescriptionThread(
        user_id=user_info["user_id"],
        team_member_user_id=user_info["team_member_user_id"]
        if "team_member_user_id" in user_info
        else None,
        admin_id=user_info["admin_id"] if "admin_id" in user_info else None,
        params=params,
        xlsx=xlsx,
        charge_credits=charge_credits,
    ).start()


@router.get(
    "/download-biosynth-product-description/{file_name}", response_class=FileResponse
)
async def download_landing_page_html(file_name: str):
    root_path = "bulk_generation_downloads"
    if exists(f"{root_path}/{file_name}.xlsx") == False:
        raise HTTPException(406, "file doesn't exist")
    return FileResponse(
        f"{root_path}/{file_name}.xlsx",
        media_type="application/octet-stream",
        filename=f"{file_name}.xlsx",
    )


@router.post("/subject-lines", response_model=schemas.OutputSubjectLineList)
def subject_lines(
    input_data: schemas.InputSubjectLine,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]

    return response_content(
        db,
        result=general_writing.SubjectLines(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/cold-emails", response_model=schemas.OutputColdEmailList)
def cold_emails(
    input_data: schemas.InputColdEmail,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.ColdEmails(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


# Cold emails V2
@router.post("/cold-emails-v2", response_model=schemas.OutputColdEmailV2List)
def cold_emails_v2(
    input_data: schemas.InputColdEmailV2,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.ColdEmailsV2(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/real-estate-listing", response_model=schemas.OutputRealEstateListingList)
def real_estate_listing(
    input_data: schemas.InputRealEstateListing,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.RealEstateListing(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/review-responses", response_model=schemas.OutputReviewResponsesList)
def review_responses(
    input_data: schemas.InputReviewResponses,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.ReviewResponses(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/quora-answers", response_model=schemas.OutputQuoraAnswerList)
def quora_answers(
    input_data: schemas.InputQuoraAnswer,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.QuoraAnswers(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/paragraph-writer", response_model=schemas.OutputParagraphWriterList)
def paragraph_writer(
    input_data: schemas.InputParagraphWriter,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=articles_and_blogs.ParagraphWriter(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/conclusion-writer", response_model=schemas.OutputConclusionWriterList)
def conclusion_writer(
    input_data: schemas.InputConclusionWriter,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=articles_and_blogs.ConclusionWriter(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/article-repharaser", response_model=schemas.OutputArticleRepharaserList)
def article_repharaser(
    input_data: schemas.InputArticleRepharaser,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]

    if input_data.link is not None:
        article = scrape_article(link=input_data.link, article=None)

    else:
        article = scrape_article(link=None, article=input_data.article)

    return response_content(
        db,
        result=articles_and_blogs.ArticleRepharaser(
            props=get_inputs(
                inputs=schemas.InputScrapedArticleRepharaser(
                    article=article, link=input_data.link
                ),
                params=params,
            ),
            user_id=user_id,
            db=db,
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/instagram-captions", response_model=schemas.OutputInstagramCaptionsList)
def instagram_captions(
    input_data: schemas.InputInstagramCaptions,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.InstagramCaptions(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/tiktok-scripts", response_model=schemas.OutputTiktokScriptsList)
def tiktok_scripts(
    input_data: schemas.InputTiktokScripts,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]

    return response_content(
        db,
        result=social_media.TiktokScripts(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/tweets", response_model=schemas.OutputTweetsList)
def tweets(
    input_data: schemas.InputTweets,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.Tweets(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/tiktok-hooks", response_model=schemas.OutputTiktokHooksList)
def tiktok_hooks(
    input_data: schemas.InputTiktokHooks,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.TiktokHooks(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/story-generation", response_model=schemas.OutputStoryGenerationList)
def story_generation(
    input_data: schemas.InputStoryGeneration,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.StoryGeneration(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/question-generation", response_model=schemas.OutputQuestionGenerationList
)
def question_generation(
    input_data: schemas.InputQuestionGeneration,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.QuestionGeneration(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/youtube-hooks", response_model=schemas.OutputYoutubeHooksList)
def youtube_hooks(
    input_data: schemas.InputYoutubeHooks,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.YoutubeHooks(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/lyrics-generator", response_model=schemas.OutputLyricsGeneratorList)
def lyrics_generator(
    input_data: schemas.InputLyricsGenerator,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.LyricsGenerator(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/define-this", response_model=schemas.OutputDefineThisList)
def define_this(
    input_data: schemas.InputDefineThis,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.DefineThis(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/youtube-intros-v2", response_model=schemas.OutputYoutubeIntrosV2List)
def youtube_intros_v2(
    input_data: schemas.InputYoutubeIntrosV2,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.YoutubeIntrosV2(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/google-ad-titles-v2", response_model=schemas.OutputGoogleAdTitleV2List)
def google_adv_titles_v2(
    input_data: schemas.InputGoogleAdTitleV2,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.GoogleAdTitlesV2(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/youtube-descriptions-v2", response_model=schemas.OutputYoutubeDescriptionsV2List
)
def youtube_descriptions_v2(
    input_data: schemas.InputYoutubeDescriptionsV2,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=social_media.YoutubeDescriptionsV2(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/google-ad-descriptions-v2", response_model=schemas.OutputGoogleAdDescriptionV2List
)
def google_adv_descriptions_v2(
    input_data: schemas.InputGoogleAdDescriptionV2,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.GoogleAdDescriptionsV2(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/bulletpoint-answers", response_model=schemas.OutputBulletpointAnswersList
)
def bulletpoint_answers(
    input_data: schemas.InputBulletpointAnswers,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.BulletpointAnswers(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/rewrite-with-keywords", response_model=schemas.OutputRewriteKeywordsList)
def rewrite_with_keywords(
    input_data: schemas.InputRewriteKeywords,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.RewriteWithKeywords(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/ans-my-ques", response_model=schemas.OutputAnsMyQuesList)
def ans_my_ques(
    input_data: schemas.InputAnsMyQues,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.AnswerMyQues(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/call-to-action", response_model=schemas.OutputCallToActionList)
def call_to_action(
    input_data: schemas.InputCallToAction,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=website_copy.CallToAction(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/app-notifications", response_model=schemas.OutputAppNotificationsList)
def app_notifications(
    input_data: schemas.InputAppNotifications,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.AppNotifications(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/pros-and-cons", response_model=schemas.OutputProsAndConsList)
def pros_and_cons(
    input_data: schemas.InputProsAndCons,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.ProsAndCons(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/active-voice", response_model=schemas.OutputActiveVoiceList)
def active_voice(
    input_data: schemas.InputActiveVoice,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=general_writing.ActiveVoice(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/linkedin-ads-v2", response_model=schemas.OutputLinkedinAdsV2List)
def linkedin_ads_v2(
    input_data: schemas.InputLinkedinAdsV2,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=ads_and_marketing_tools.LinkedinAdsV2(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post(
    "/instant-article-writer", response_model=schemas.OutputInstantArticleWriterList
)
def instant_article_writer(
    input_data: schemas.InputInstantArticleWriter,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=articles_and_blogs.InstantArticleWriter(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )


@router.post("/review-generator", response_model=schemas.OutputReviewGeneratorList)
def review_generator(
    input_data: schemas.InputReviewGenerator,
    user_info=Depends(deps.get_user_info),
    params=Depends(deps.get_content_parameters),
    pagination_params=Depends(deps.get_pagination_params),
    db: Session = Depends(deps.get_db),
) -> Dict:
    user_id = user_info["user_id"]
    if "admin_id" in user_info:
        params["admin_id"] = user_info["admin_id"]
    return response_content(
        db,
        result=other.ReviewGenerator(
            props=get_inputs(inputs=input_data, params=params), user_id=user_id, db=db
        ).generate(db=db),
        pagination_params=pagination_params if params["paginate"] == True else None,
    )
